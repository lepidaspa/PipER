# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'DataModelAttributeSemantic'
        db.delete_table('model_manager_datamodelattributesemantic')

        # Deleting model 'DataModelAttributeTable'
        db.delete_table('model_manager_datamodelattributetable')

        # Deleting model 'DataModelAttributeValues'
        db.delete_table('model_manager_datamodelattributevalues')

        # Adding model 'Infrastructure'
        db.create_table('model_manager_infrastructure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('model_manager', ['Infrastructure'])

        # Deleting field 'DataModelAttribute.semantic'
        db.delete_column('model_manager_datamodelattribute', 'semantic_id')


    def backwards(self, orm):
        # Adding model 'DataModelAttributeSemantic'
        db.create_table('model_manager_datamodelattributesemantic', (
            ('filter', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('related_table_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['model_manager.DataModelAttributeTable'], null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('model_manager', ['DataModelAttributeSemantic'])

        # Adding model 'DataModelAttributeTable'
        db.create_table('model_manager_datamodelattributetable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('model_manager', ['DataModelAttributeTable'])

        # Adding model 'DataModelAttributeValues'
        db.create_table('model_manager_datamodelattributevalues', (
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['model_manager.DataModelAttributeTable'])),
            ('super', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', null=True, to=orm['model_manager.DataModelAttributeValues'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('model_manager', ['DataModelAttributeValues'])

        # Deleting model 'Infrastructure'
        db.delete_table('model_manager_infrastructure')

        # Adding field 'DataModelAttribute.semantic'
        db.add_column('model_manager_datamodelattribute', 'semantic',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['model_manager.DataModelAttributeSemantic'], null=True, blank=True),
                      keep_default=False)


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
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'model_manager.datamodelcontainer': {
            'Meta': {'object_name': 'DataModelContainer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'model_manager.infrastructure': {
            'Meta': {'object_name': 'Infrastructure'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['model_manager']