#  encoding: utf-8

__author__ = 'alexaled'

import yaml

from django.db import models

from smyttest import settings
import modelsutils


def create_models():
    """
    Function create models from yaml file description
    """
    file_name = settings.MODELS_YAML_FILE
    models_list_loc = {}
    with file(file_name, 'r') as model_file:
        file_data = yaml.safe_load(model_file)
        for data in file_data:
            table_data = file_data[data]
            attributes = {'__module__': __name__}

            fields = table_data.get('fields', [])
            title = table_data.get('title', data)

            attributes['Meta'] = type('Meta', (),
                                      {'verbose_name_plural': title,
                                       'verbose_name': title})

            for field in fields:
                attributes[field['id']] = modelsutils.set_field(field)

            # id must be first element
            fields.insert(0, {'id': 'id', 'title': 'id', 'type': 'int'})

            model_class = type(data, (models.Model,), attributes)
            models_list_loc[data] = {'title': title, 'class': model_class, 'fields': fields}

    return models_list_loc


def update_object(model_name, obj_id, field, value):
    """
    Function update object field from table cell and return update status
    """
    model_class = models_data[model_name].get('class', None)
    if model_class:
        object_upd = model_class.objects.get(pk=int(obj_id))
        setattr(object_upd, field, value)
        object_upd.save()
        return True
    else:
        return False


models_data = create_models()
