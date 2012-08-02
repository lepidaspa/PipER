# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DataModel.within'
        db.add_column('model_manager_datamodel', 'within',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='contains', null=True, to=orm['model_manager.DataModel']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DataModel.within'
        db.delete_column('model_manager_datamodel', 'within_id')


    models = {
        'model_manager.datamodel': {
            'Meta': {'object_name': 'DataModel'},
            'container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'models'", 'to': "orm['model_manager.DataModelContainer']"}),
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
            'semantic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['model_manager.DataModelAttributeSemantic']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'model_manager.datamodelattributesemantic': {
            'Meta': {'object_name': 'DataModelAttributeSemantic'},
            'filter': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'related_table_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['model_manager.DataModelAttributeTable']", 'null': 'True', 'blank': 'True'})
        },
        'model_manager.datamodelattributetable': {
            'Meta': {'object_name': 'DataModelAttributeTable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'model_manager.datamodelattributevalues': {
            'Meta': {'object_name': 'DataModelAttributeValues'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'super': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['model_manager.DataModelAttributeValues']"}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['model_manager.DataModelAttributeTable']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'model_manager.datamodelcontainer': {
            'Meta': {'object_name': 'DataModelContainer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['model_manager']