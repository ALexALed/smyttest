#  encoding: utf-8

__author__ = 'alexaled'

import datetime
import json

from django.test import TestCase
from django.test.client import Client
from django.utils import timezone

from models import models_list, get_model_class_by_name
from modelsutils import get_fields_names_types
from testapp import modelsutils


class ModelsRequestTests(TestCase):
    """Models and request tests."""

    def test_models(self):
        default_values = {'int': 100, 'char': 'val', 'date': timezone.now()}

        for model in models_list:
            model_fields_types = get_fields_names_types(model)
            model_object = model()
            for field in model_fields_types:
                if field['name'] == 'id':
                    continue
                setattr(model_object, field['name'],
                        default_values[field['type']])

            model_object.save()

            new_object = model.objects.all().count()

            self.assertEquals(new_object, 1, 'not save object in db')

    def test_request(self):
        # create objects
        self.test_models()
        new_date = timezone.now().date()-datetime.timedelta(days=1)
        defaults_values = {'int': 200, 'char': 'valchanged',
                           'date': new_date}
        client = Client()

        response = client.get('/')
        self.assertEqual(response.status_code, 200, 'response code not valid')

        models_names = modelsutils.get_models_names_titles(models_list)

        for table in models_names:
            response = client.post('/table-content/'+table['name']+'/',
                                   {'value': '1'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200,
                             'response code not valid')
            self.assertContains(response, table['name'])

            model_class = get_model_class_by_name(table['name'])
            model_fields_types = get_fields_names_types(model_class)
            field = model_fields_types[1]
            send_data = {'table': table['name'],
                         'field': field['name'],
                         'object_id': 1,
                         'value': defaults_values[field['type']]}
            response = client.post('/table-post/', send_data,
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200,
                             'response code not valid')
            self.assertEqual(
                getattr(model_class.objects.get(pk=1), field['name']),
                defaults_values[field['type']],
                'model object not contains new value')

            object_data = []
            for field in model_fields_types:
                if field['name'] == 'id':
                    continue
                object_data.append(
                    {'name': field['name'], 'value':
                        unicode(defaults_values[field['type']])})

            send_data = {'table': table['name'],
                         'object_data': json.dumps(object_data)}
            response = client.post('/new-post/',  send_data,
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            self.assertEqual(response.status_code, 200,
                             'response code not valid')
            self.assertEqual(model_class.objects.get(pk=2).id, 2,
                             'model object not contains new object')
