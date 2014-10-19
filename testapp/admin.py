#  encoding: utf-8

__author__ = 'alexaled'

from django.contrib import admin
from models import models_data

admin.site.register([models_data[model]['class'] for model in models_data])
