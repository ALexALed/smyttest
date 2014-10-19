#  encoding: utf-8

__author__ = 'alexaled'

import json

from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.urlresolvers import reverse

import models


def home(request):
    models_titles = [{'name': model_name,
                      'verbose_name': models.models_data[model_name].get('title')}
                     for model_name in models.models_data]
    return render_to_response("base.html", {'tables': models_titles})


@ensure_csrf_cookie
def table_content(request, table_class_name):
    model_data = models.models_data.get(table_class_name, None)
    model_class = model_data['class']

    if not model_class:
        raise Http404

    # get class attributes and types
    models_fields = model_data['fields']

    models_objects = model_class.objects.all()

    json_objects = serializers.serialize("json", models_objects)
    send_data = {'success': True, 'tableName': table_class_name, 'fields': models_fields,
                 'tableData': json_objects}

    return HttpResponse(json.dumps(send_data), content_type="application/json")


@ensure_csrf_cookie
def table_post(request):
    if request.POST and request.is_ajax():
        try:
            table = request.POST[u'table']
            field = request.POST[u'field']
            obj_id = request.POST[u'object_id']
            value = request.POST[u'value']
            result = models.update_object(table, obj_id, field, value)
            send_data = {'success': result}
        except:
            send_data = {'success': False}

        return HttpResponse(json.dumps(send_data), content_type="application/json")
    else:
        raise Http404


@ensure_csrf_cookie
def new_post(request):
    if request.POST and request.is_ajax():
        try:
            table = request.POST[u'table']
            model_data = models.models_data.get(table, None)
            model_class = model_data['class']
            object_data = json.loads(request.POST['object_data'])
            model_object = model_class()
            for field_dict in object_data:
                setattr(model_object, field_dict['name'], field_dict['value'])
            model_object.save()
            send_data = {'success': True, 'link': reverse('table-content', args=[table])}
        except:
            send_data = {'success': False}
        return HttpResponse(json.dumps(send_data), content_type="application/json")

    else:
        raise Http404
