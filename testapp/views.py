#encoding: utf-8

__author__ = 'alexaled'

import json

from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse

import models
import modelsutils


def home(request):
    models_titles = modelsutils.get_models_names_titles(models.models_list)
    return render_to_response("index.html", {'tables': models_titles})


def table_content(request, table_class_name):
    model_class = models.get_model_class_by_name(table_class_name)

    if not model_class:
        raise Http404

    # get class attributes and types
    models_fields = modelsutils.get_fields_names_types(model_class)

    models_objects = model_class.objects.all()

    json_objects = serializers.serialize("json", models_objects)
    send_data = {'success': True, 'tableName': table_class_name, 'fields': models_fields,
                 'tableData': json_objects}

    return HttpResponse(json.dumps(send_data), content_type="application/json")


@csrf_protect
def table_post(request):
    if request.POST and request.is_ajax():
        table = request.POST[u'table']
        field = request.POST[u'field']
        obj_id = request.POST[u'object_id']
        value = request.POST[u'value']
        models.update_object(table, obj_id, field, value)
        send_data = {'success': True}
        return HttpResponse(json.dumps(send_data), content_type="application/json")
    else:
        raise Http404


@csrf_protect
def new_post(request):
    if request.POST and request.is_ajax():
        table = request.POST[u'table']
        object_data = json.loads(request.POST['object_data'])
        model_class = models.get_model_class_by_name(table)
        model_object = model_class()
        for field_dict in object_data:
            setattr(model_object, field_dict['name'], field_dict['value'])
        model_object.save()
        send_data = {'success': True, 'link': reverse('table-content', args=[table])}
        return HttpResponse(json.dumps(send_data), content_type="application/json")
    else:
        raise Http404

