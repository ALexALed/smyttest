__author__ = 'alexaled'

from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^table-content/(?P<table_class_name>[A-Za-z]*)/$', 'testapp.views.table_content', name='table-content'),
    url(r'^table-post/$', 'testapp.views.table_post', name='table-post'),
    url(r'^new-post/$', 'testapp.views.new_post', name='new-post'),
    url(r'^$', 'testapp.views.home', name='home'),
)
