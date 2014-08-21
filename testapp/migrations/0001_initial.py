# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'users'
        db.create_table(u'testapp_users', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'', max_length=150)),
            ('paycheck', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date_joined', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'testapp', ['users'])

        # Adding model 'rooms'
        db.create_table(u'testapp_rooms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.CharField')(default=u'', max_length=150)),
            ('spots', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'testapp', ['rooms'])


    def backwards(self, orm):
        # Deleting model 'users'
        db.delete_table(u'testapp_users')

        # Deleting model 'rooms'
        db.delete_table(u'testapp_rooms')


    models = {
        u'testapp.rooms': {
            'Meta': {'object_name': 'rooms'},
            'department': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'testapp.users': {
            'Meta': {'object_name': 'users'},
            'date_joined': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '150'}),
            'paycheck': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['testapp']