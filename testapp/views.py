from django.shortcuts import render_to_response
from models import modelslist
from django.db import models
from django.http import HttpResponse

import json

def home(request):
    models_titles = [(model._meta.verbose_name.title(), model.__name__) for model in modelslist]
    return render_to_response("home.html", {'tables': models_titles})

def table_content(request, table_class_name):
    modelclass = None
    for table in modelslist:
        if table.__name__ == table_class_name:
            modelclass = table
            break


    #get class attributes and types
    models_fields_type={}
    for attr in modelclass._meta.fields:
        field_class = attr.__class__
        if field_class == models.fields.AutoField:
            continue
        field_type = None
        if field_class == models.fields.CharField:
            field_type = 'char'
        elif field_class == models.fields.IntegerField:
            field_type = 'int'
        elif field_class == models.fields.DateField:
            field_type = 'date'

        models_fields_type[attr.attname] = field_type

    models_objects = modelclass.objects.all()

    send_data = {'tablename': table_class_name, 'fields': models_fields_type, 'tabledata': models_objects}

    return HttpResponse(json.dump(send_data), content_type="application/json")


