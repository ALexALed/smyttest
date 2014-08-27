import yaml
from django.db import models
from smyttest import settings
import modelsutils


def create_models():
    '''
    Function create models from yaml file description
    '''
    file_name = settings.MODELS_YAML_FILE
    modelslist = []
    with file(file_name, 'r') as model_file:
        file_data = yaml.safe_load(model_file)
        for data in file_data:
            rdata = file_data[data]
            attributes = {'__module__': __name__}

            fields = rdata.pop('fields', [])
            title = rdata.pop('title', data)

            attributes['Meta'] = type('Meta', (), {'verbose_name_plural': title, 'verbose_name': title})

            for field in fields:
                attributes[field['id']] = modelsutils.set_field(field)

            modelclass = type(data, (models.Model,), attributes)
            modelslist.append(modelclass)

    return modelslist

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

def update_object(modelname, id, field, value):
    modelclass = get_modelclass_by_name(modelname)
    object_upd = modelclass.objects.get(pk=int(id))
    setattr(object_upd, field, value)
    object_upd.save()


modelslist = create_models()
__all__ = modelslist
