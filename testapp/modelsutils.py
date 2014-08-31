#encoding: utf-8

__author__ = 'alexaled'

from django.utils import timezone
from django.db import models


FIELDS_TYPES = {
    'char': (models.CharField, {'max_length': 150, 'default': u''}),
    'int':  (models.IntegerField, {'default': 0}),
    'date': (models.DateField, {'default': timezone.now()})
}


def set_field(field):
    """
    Function set model field type, verbose_name and args
    """
    field_type = field.pop('type')
    field_class, field_kwargs = FIELDS_TYPES[field_type]
    field_kwargs['verbose_name'] = field.pop('title', field_type)

    return field_class(**field_kwargs)


def get_fields_names_types(model_class):
    """
    Function return list of fields for model class
    """
    models_fields = []
    for attr in model_class._meta.fields:
        field_class = attr.__class__
        if field_class == models.fields.AutoField:
            field_type = 'int'
        if field_class == models.fields.CharField:
            field_type = 'char'
        elif field_class == models.fields.IntegerField:
            field_type = 'int'
        elif field_class == models.fields.DateField:
            field_type = 'date'

        models_fields.append({'name': attr.attname, 'type': field_type, 'verbose_name': attr.verbose_name})

    return models_fields


def get_models_names_titles(models_list):
    """
    Function return list of dict with name and verbose_name for models
    """
    return [{'name': model.__name__, 'verbose_name': model._meta.verbose_name.title()} for model in models_list]

