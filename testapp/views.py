import json
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
import models
import modelsutils


def home(request):
    models_titles = [(model._meta.verbose_name.title(), model.__name__) for model in models.modelslist]
    return render_to_response("index.html", {'tables': models_titles})


def table_content(request, table_class_name):

    modelclass = models.get_modelclass_by_name(table_class_name)

    if not modelclass:
        raise Http404

    #get class attributes and types
    models_fields = modelsutils.get_fields_names_types(modelclass)

    models_objects = modelclass.objects.all()

    json_objects = serializers.serialize("json", models_objects)
    send_data = {'success': True, 'tablename': table_class_name, 'fields': models_fields,
                 'tabledata': json_objects}

    return HttpResponse(json.dumps(send_data), content_type="application/json")

@csrf_protect
def table_post(request):
    if request.POST and request.is_ajax():
        table = request.POST[u'table']
        field = request.POST[u'field']
        id = request.POST[u'object_id']
        value = request.POST[u'value']
        models.update_object(table, id, field, value)
        send_data = {'success': True}
        return HttpResponse(json.dumps(send_data), content_type="application/json")
    else:
        raise Http404

@csrf_protect
def new_post(request):
    if request.POST and request.is_ajax():
        table = request.POST[u'table']
        objectdata = json.loads(request.POST['object_data'])
        modelclass = models.get_modelclass_by_name(table)
        instanse = modelclass()
        for fielddict in objectdata:
            setattr(instanse, fielddict['name'], fielddict['value'])
        instanse.save()
        send_data = {'success': True, 'link': reverse('table-content', args=[table])}
        return HttpResponse(json.dumps(send_data), content_type="application/json")
    else:
        raise Http404


