#encoding: utf-8

__author__ = 'alexaled'

import datetime
from django.db import models
from models import modelslist


fields_types = {
    'char': (models.CharField, {'max_length': 150, 'default': u''}),
    'int':  (models.IntegerField, {'default': 0}),
    'date': (models.DateField, {'default': datetime.datetime.now()})
}


def set_field(field):
    '''
    Function set model field type, verbose_name and args
    '''
    field_type = field.pop('type')
    field_class, field_kwargs = fields_types[field_type]
    field_kwargs['verbose_name'] = field.pop('title', field_type)
    return field_class(**field_kwargs)


def get_fields_names_types(modelclass):
    '''
    Function return list of fields for model class
    '''
    models_fields = []
    for attr in modelclass._meta.fields:
        field_class = attr.__class__
        if field_class == models.fields.AutoField:
            field_type = 'int'
        if field_class == models.fields.CharField:
            field_type = 'char'
        elif field_class == models.fields.IntegerField:
            field_type = 'int'
        elif field_class == models.fields.DateField:
            field_type = 'date'

        models_fields.append({'name': attr.attname, 'type': field_type})
    return models_fields


def get_modelclass_by_name(classname):
    '''
    Function find class by class name in models class list
    '''
    modelclass = None
    for table in modelslist:
        if table.__name__ == classname:
            modelclass = table
            break
    return modelclass