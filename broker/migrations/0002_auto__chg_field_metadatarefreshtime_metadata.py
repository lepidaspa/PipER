# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'MetadataRefreshTime.metadata'
        db.alter_column('broker_metadatarefreshtime', 'metadata_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['broker.Proxy']))

    def backwards(self, orm):

        # Changing field 'MetadataRefreshTime.metadata'
        db.alter_column('broker_metadatarefreshtime', 'metadata_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['broker.Metadata']))

    models = {
        'broker.metadata': {
            'BB_east': ('django.db.models.fields.FloatField', [], {}),
            'BB_north': ('django.db.models.fields.FloatField', [], {}),
            'BB_south': ('django.db.models.fields.FloatField', [], {}),
            'BB_west': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'object_name': 'Metadata'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'proxy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'metadata'", 'to': "orm['broker.Proxy']"})
        },
        'broker.metadatarefreshtime': {
            'Meta': {'object_name': 'MetadataRefreshTime'},
            'crontab': ('django.db.models.fields.TextField', [], {'default': "'0 1 * * SAT'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['broker.Proxy']"})
        },
        'broker.proxy': {
            'Meta': {'object_name': 'Proxy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manifest': ('django.db.models.fields.TextField', [], {}),
            'mode_query': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mode_read': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mode_write': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'request': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'data'", 'unique': 'True', 'to': "orm['broker.ProxyRequest']"})
        },
        'broker.proxyrequest': {
            'Meta': {'object_name': 'ProxyRequest'},
            'token': ('django.db.models.fields.TextField', [], {'unique': 'True', 'primary_key': 'True', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['broker']