#  encoding: utf-8

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
    field_type = field.get('type', '')
    field_class, field_kwargs = FIELDS_TYPES[field_type]
    field_kwargs['verbose_name'] = field.get('title', field_type)

    return field_class(**field_kwargs)