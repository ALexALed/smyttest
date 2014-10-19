$(document).ready(function () {
    $('#msg').dialog();
    $('#msg').dialog({ buttons: [
        { text: "Ok", click: function () {
            $(this).dialog("close");
        } }
    ] });
    $('#msg').dialog('close');

    var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken || $.cookie('csrftoken'));
            }
        }
    });

    $('.tablelink').click(function () {
        $.get($(this).attr('id'), function (data) {
            fillTable(data.tableName, data.fields, data.tableData);
            fillNewForm(data.tableName, data.fields);
        });
    });

    function parseClasses(element) {
        var arrClasses = element.attr('class').split(' ');
        var cellType = '';
        var cellName = '';
        var elClass = null;
        for (elClass in arrClasses) {
            if (arrClasses[elClass] == 'int' || arrClasses[elClass] == 'char' || arrClasses[elClass] == 'date') {
                cellType = arrClasses[elClass];
            } else {
                cellName = arrClasses[elClass];
            }
        }
        return {type: cellType, name: cellName};
    }

    function sendNewValue(tableName, fieldName, rowId, valueNew) {
        $.ajax({url: '/table-post/',
                type: "POST",
                data: {table: tableName,
                    field: fieldName,
                    object_id: rowId,
                    value: valueNew},
                success: function (data) {
                    if (data.success) {
                        $('#msg').empty();
                    } else {
                        showErrorMessage('Ошибка при сохранении на сервере!');
                    }
                }}
        );
    }

    function onCellClick(element) {
        if ($('#inp').length > 0) {
            return;
        }
        var value = element.text();
        var cellProps = parseClasses(element);
        var cellType = cellProps.type;
        var cellName = cellProps.name;

        if (cellName == 'id') {
            return;
        }

        element.empty();
        element.append('<input type="text" id="inp" name="' + cellName + '" class = "' + cellType + '" value = "' + value + '"/>');

        if (cellType == 'date') {
            var val = $('#inp').val();
            makeDatePicker($('#inp'), val);
            $('#inp').datepicker('option', {onClose: function () {
                var parent = $(this).parent();
                parent.empty();
                parent.text(val);
            }});
        }

        $('#inp').focus();

        $('#inp').change(function (event) {
            var table = $('#activetable');
            var tableName = table.attr('class');
            var rowId = element.parent().children('.id').text();
            var parent = $(this).parent();
            var valueType = parseClasses($(this)).type;
            var valueNew = $(this).val();
            var fieldName = $(this).attr('name');

            var valid = validateValue(valueNew, valueType);

            if (valid) {
                sendNewValue(tableName, fieldName, rowId, valueNew);
                parent.empty();
                parent.text(valueNew);
            } else {
                showErrorMessage('Введено неверное значение ' + valueNew + '!');
                $('#inp').addClass('mistake');
                $('#inp').focus();
            }

        });

        $('#inp').focusout(function (event) {

            if (cellType == 'date') {
                return;
            }

            var previousValue = event.currentTarget.defaultValue;
            var parent = $(this).parent();
            parent.empty();
            parent.text(previousValue);
        });
    }

    function showErrorMessage(message) {
        $('#msg').empty();
        $('#msg').append('<p>' + message + '</p>');
        $('#msg').dialog('open');
    }

    function newFormFieldEvents(element) {

        var valueType = parseClasses(element).type;
        var valueNew = element.val();
        var valid = validateValue(valueNew, valueType);
        if (valid) {
            element.removeClass('mistake');
            element.val(valueNew);
        } else {
            showErrorMessage('Введено неверное значение ' + valueNew + '!');
            element.addClass('mistake');
            element.focus();
        }
    }

    function validateValue(value, valueType) {
        if (valueType == 'int') {
            return !isNaN(parseInt(value)) && isFinite(value)
        } else if (valueType == 'date') {
            return isValidDate(value);
        } else if (valueType == 'char') {
            var letters = /^[0-9a-zA-Zа-яА-Я]+$/;
            var newValue = value.replace(/\s+/g, '');
            return newValue.match(letters);
        }
    }

    function isValidDate(date) {
        var matches = /^(\d{4})[-\/](\d{2})[-\/](\d{2})$/.exec(date);
        if (matches == null) return false;
        var d = matches[3];
        var m = matches[2];
        var y = matches[1] - 1;
        var composedDate = new Date(y, m, d);
        return composedDate.getDate() == d &&
            composedDate.getMonth() == m &&
            composedDate.getFullYear() == y;
    }

    function fillTable(tablename, fields, tabledata) {
        var table = $('#activetable');
        table.attr('class', tablename);
        //clean table
        table.empty();
        //table headers
        var headers = '<tr>';
        var field = null;
        for (field in fields) {
            headers += '<th>' + fields[field].title + '</th>';
        }
        headers += '</tr>';
        //table rows
        var rowdata = null;
        var rows = '';
        tabledata = JSON.parse(tabledata);
        for (rowdata in tabledata) {
            var row = '<tr>';
            for (field in fields) {
                var cellvalue = '';
                if (fields[field].id == 'id') {
                    cellvalue = tabledata[rowdata]['pk'];
                } else {
                    cellvalue = tabledata[rowdata].fields[[fields[field].id]];
                }
                row += '<td class = "' + fields[field].id + ' ' + fields[field].type + '">' + cellvalue + '</td>';
            }
            row += '</tr>';
            rows += row;
        }
        table.html(headers + rows);

        $('td').click(function () {
            onCellClick($(this));
        });
    }

    function fillNewForm(tablename, fields) {
        $('#newform').empty();
        $('#newform').attr('class', tablename);
        for (field in fields) {
            if (fields[field].id == 'ID' || fields[field].id == 'id') {
                continue;
            }
            $('#newform').append('<label>' + fields[field].title + '<input class=' + fields[field].type + ' type=text name=' + fields[field].id + ' /></label><br>');
        }

        $('#newform').append('<input id="submit" type="submit"  value="Добавить">');

        $('#newform').find("input,select").not('[type="submit"]').each(function () {

            if ($(this).hasClass('date')) {
                makeDatePicker($(this), $(this).val());
            }

            $(this).change(function () {
                newFormFieldEvents($(this));
            });
        });

        $('#newform').submit(function () {
            return false;
        });

        $('#submit').click(function () {
            $('#submit').attr('disabled', true);
            var table_name = $('#newform').attr('class');
            var haveMistakes = false;
            $('#newform').find("input,select").not('[type="submit"]').each(function () {
                var valueType = parseClasses($(this)).type;
                var valid = validateValue($(this).val(), valueType)
                if (!valid) {
                    haveMistakes = true;
                    $(this).addClass('mistake');
                }
            });

            if (haveMistakes) {
                showErrorMessage('Ошибка при заполнении формы!');
                $('#submit').attr('disabled', false);
                return;
            }
            sendNewRowData(table_name, JSON.stringify($('#newform').serializeArray()));
            $('#submit').attr('disabled', false);
        });
    }

    function sendNewRowData(table_name, formDataJSON) {
        var newUrl = $('#newform').attr('action');
        $.post(newUrl, {table: table_name, object_data: formDataJSON},
            function (data) {
                $.get(data.link, function (data) {
                    if (data.success) {
                        $('#msg').empty();
                    } else {
                        showErrorMessage('Ошибка при сохранении на сервере!');
                    }
                    fillTable(data.tableName, data.fields, data.tableData);
                    fillNewForm(data.tableName, data.fields);
                });
            }
        );
    }

    function makeDatePicker(element, intVal) {
        element.datepicker();
        element.datepicker('option', 'dateFormat', 'yy-mm-dd');
        element.datepicker("setDate", intVal);
        element.keydown(function () {
            return false;
        });
    }

});