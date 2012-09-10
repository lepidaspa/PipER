# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataModelContainer'
        db.create_table('model_manager_datamodelcontainer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('model_manager', ['DataModelContainer'])

        # Adding model 'DataModel'
        db.create_table('model_manager_datamodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('container', self.gf('django.db.models.fields.related.ForeignKey')(related_name='models', to=orm['model_manager.DataModelContainer'])),
            ('federated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('within', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='contains', null=True, to=orm['model_manager.DataModel'])),
            ('geo_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('model_manager', ['DataModel'])

        # Adding model 'DataModelAttributeTable'
        db.create_table('model_manager_datamodelattributetable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('model_manager', ['DataModelAttributeTable'])

        # Adding model 'DataModelAttributeValues'
        db.create_table('model_manager_datamodelattributevalues', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['model_manager.DataModelAttributeTable'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('super', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['model_manager.DataModelAttributeValues'])),
        ))
        db.send_create_signal('model_manager', ['DataModelAttributeValues'])

        # Adding model 'DataModelAttributeSemantic'
        db.create_table('model_manager_datamodelattributesemantic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filter', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('related_table_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['model_manager.DataModelAttributeTable'], null=True, blank=True)),
        ))
        db.send_create_signal('model_manager', ['DataModelAttributeSemantic'])

        # Adding model 'DataModelAttribute'
        db.create_table('model_manager_datamodelattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_model', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attributes', to=orm['model_manager.DataModel'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('semantic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['model_manager.DataModelAttributeSemantic'], null=True, blank=True)),
        ))
        db.send_create_signal('model_manager', ['DataModelAttribute'])


    def backwards(self, orm):
        # Deleting model 'DataModelContainer'
        db.delete_table('model_manager_datamodelcontainer')

        # Deleting model 'DataModel'
        db.delete_table('model_manager_datamodel')

        # Deleting model 'DataModelAttributeTable'
        db.delete_table('model_manager_datamodelattributetable')

        # Deleting model 'DataModelAttributeValues'
        db.delete_table('model_manager_datamodelattributevalues')

        # Deleting model 'DataModelAttributeSemantic'
        db.delete_table('model_manager_datamodelattributesemantic')

        # Deleting model 'DataModelAttribute'
        db.delete_table('model_manager_datamodelattribute')


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