#encoding: utf-8

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
    models_list_loc = []
    with file(file_name, 'r') as model_file:
        file_data = yaml.safe_load(model_file)
        for data in file_data:
            table_data = file_data[data]
            attributes = {'__module__': __name__}

            fields = table_data.pop('fields', [])
            title = table_data.pop('title', data)

            attributes['Meta'] = type('Meta', (), {'verbose_name_plural': title, 'verbose_name': title})

            for field in fields:
                attributes[field['id']] = modelsutils.set_field(field)

            model_class = type(data, (models.Model,), attributes)
            models_list_loc.append(model_class)

    return models_list_loc


def get_model_class_by_name(class_name):
    """
    Function find class by class name in models class list
    """
    model_class = None
    for table in models_list:
        if table.__name__ == class_name:
            model_class = table
            break
    return model_class


def update_object(model_name, obj_id, field, value):
    """
    Function update object field from table cell
    """
    model_class = get_model_class_by_name(model_name)
    object_upd = model_class.objects.get(pk=int(obj_id))
    setattr(object_upd, field, value)
    object_upd.save()


models_list = create_models()

