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
            #globals()[data] = modelclass
    return modelslist


modelslist = create_models()
__all__ = modelslist
