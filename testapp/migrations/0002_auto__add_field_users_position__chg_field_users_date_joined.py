# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'users.position'
        db.add_column(u'testapp_users', 'position',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=150),
                      keep_default=False)


        # Changing field 'users.date_joined'
        db.alter_column(u'testapp_users', 'date_joined', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):
        # Deleting field 'users.position'
        db.delete_column(u'testapp_users', 'position')


        # Changing field 'users.date_joined'
        db.alter_column(u'testapp_users', 'date_joined', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

    models = {
        u'testapp.rooms': {
            'Meta': {'object_name': 'rooms'},
            'department': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'testapp.users': {
            'Meta': {'object_name': 'users'},
            'date_joined': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 8, 25, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '150'}),
            'paycheck': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '150'})
        }
    }

    complete_apps = ['testapp']