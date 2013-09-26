# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DataModelContainer'
        db.delete_table('model_manager_datamodelcontainer')


        # Changing field 'DataModel.container'
        db.alter_column('model_manager_datamodel', 'container_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['model_manager.DataModel']))

    def backwards(self, orm):
        # Adding model 'DataModelContainer'
        db.create_table('model_manager_datamodelcontainer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('model_manager', ['DataModelContainer'])


        # Changing field 'DataModel.container'
        db.alter_column('model_manager_datamodel', 'container_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['model_manager.DataModelContainer']))

    models = {
        'model_manager.datamodel': {
            'Meta': {'object_name': 'DataModel'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'models'", 'null': 'True', 'to': "orm['model_manager.DataModel']"}),
            'federated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geo_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'within': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contains'", 'null': 'True', 'to': "orm['model_manager.DataModel']"})
        },
        'model_manager.datamodelattribute': {
            'Meta': {'object_name': 'DataModelAttribute'},
            'data_model': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attributes'", 'to': "orm['model_manager.DataModel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'model_manager.infrastructure': {
            'Meta': {'object_name': 'Infrastructure'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['model_manager']