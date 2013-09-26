# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Proxy.name'
        db.add_column('broker_proxy', 'name',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Proxy.name'
        db.delete_column('broker_proxy', 'name')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'broker.metadata': {
            'BB_east': ('django.db.models.fields.FloatField', [], {}),
            'BB_north': ('django.db.models.fields.FloatField', [], {}),
            'BB_south': ('django.db.models.fields.FloatField', [], {}),
            'BB_west': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'object_name': 'Metadata'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'proxy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'metadata'", 'to': "orm['broker.Proxy']"})
        },
        'broker.metadatarefreshtime': {
            'Meta': {'object_name': 'MetadataRefreshTime'},
            'crontab': ('django.db.models.fields.TextField', [], {'default': "'0 1 * * SAT'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'timing'", 'unique': 'True', 'to': "orm['broker.Proxy']"})
        },
        'broker.owner': {
            'Meta': {'object_name': 'Owner'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'broker.ownerdata': {
            'Meta': {'object_name': 'OwnerData'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['broker.Owner']", 'unique': 'True'}),
            'referral_email': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'referral_name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'broker.proxy': {
            'Meta': {'object_name': 'Proxy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manifest': ('django.db.models.fields.TextField', [], {}),
            'mode_query': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mode_read': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mode_write': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'request': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'data'", 'unique': 'True', 'to': "orm['broker.ProxyRequest']"})
        },
        'broker.proxyrequest': {
            'Meta': {'object_name': 'ProxyRequest'},
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'proxies'", 'null': 'True', 'to': "orm['broker.Owner']"}),
            'token': ('django.db.models.fields.TextField', [], {'unique': 'True', 'primary_key': 'True', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['broker']