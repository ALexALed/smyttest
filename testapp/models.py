import datetime
from django.db import models
from smyttest import settings

modelslist = []

fields_types = {
    'char': (models.CharField, {'max_length': 150, 'default': u''}),
    'int':  (models.IntegerField, {'default': 0}),
    'date': (models.DateField, {'default': datetime.datetime.now()})
}


def create_models():
    '''
    Function create models from yaml file description
    '''
    import yaml

    file_name = settings.MODELS_YAML_FILE

    with file(file_name, 'r') as model_file:
        file_data = yaml.safe_load(model_file)
        for data in file_data:
            rdata = file_data[data]
            attributes = {'__module__': __name__}

            fields = rdata.pop('fields', [])
            title = rdata.pop('title', data)

            attributes['Meta'] = type('Meta', (), {'verbose_name_plural': title, 'verbose_name': title})

            for field in fields:
                attributes[field['id']] = set_field(field)

            modelclass = type(data, (models.Model,), attributes)
            modelslist.append(modelclass)
            globals()[data] = modelclass


def set_field(field):
    '''
    Function set model field type, verbose_name and args
    '''
    field_type = field.pop('type')
    field_class, field_kwargs = fields_types[field_type]
    field_kwargs['verbose_name'] = field.pop('title', field_type)
    return field_class(**field_kwargs)

create_models()
__all__ = modelslist
