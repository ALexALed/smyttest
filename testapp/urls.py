__author__ = 'alexaled'

from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'testapp.views.home', name='home'),
    url(r'^$', 'testapp.views.home', name='home'),

)
