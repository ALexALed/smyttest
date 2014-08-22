import json
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.core import serializers
from models import modelslist
import modelsutils


def home(request):
    models_titles = [(model._meta.verbose_name.title(), model.__name__) for model in modelslist]
    return render_to_response("index.html", {'tables': models_titles})


def table_content(request, table_class_name):

    modelclass = modelsutils.get_modelclass_by_name(table_class_name)

    if not modelclass:
        raise Http404

    #get class attributes and types
    models_fields = modelsutils.get_fields_names_types(modelclass)

    models_objects = modelclass.objects.all()

    json_objects = serializers.serialize("json", models_objects)
    send_data = {'tablename': table_class_name, 'fields': models_fields, 'tabledata': json_objects}

    return HttpResponse(json.dumps(send_data), content_type="application/json")


