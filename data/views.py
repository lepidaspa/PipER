# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt

import pymongo

from django.contrib.gis.gdal import OGRGeometry
from pymongo import Connection


def put_data(data):
    """
    {
        u"token": unicode,
        u"message_type": (u'response',),
        u"message_format": (u'read',),
        u"data": {
            u"upserts": {
                "metadata_name": /GEOJSON - FeatureCollection/,
                "metadata_name": /GEOJSON - FeatureCollection/,
                "metadata_name": /GEOJSON - FeatureCollection/
            },
            u"delete": list /generalmente vuota/
        }
    }
    """
    
    connection = Connection()
    db = connection.data
    
    token_id = data['token']
    collection = db['elements']
    
    #do coorections on data wwith specific elements...
    #avoid duplicates
    
    for metadata_name, featurecollection in data['data']['upserts'].items():
        for fc in featurecollection:
            for feature in fc['features']:
                polygon = OGRGeometry(json.dumps(feature['geometry']))
                feature['_center'] = json.loads(polygon.geos.centroid.json)
                feature['_proxy'] = token_id
                feature['_metadata'] = metadata_name
                collection.insert(feature)
            
    return HttpResponse()
            
def run_query(bb, query):
    connection = Connection()
    db = connection.data
    collection = db['elements']
    
    print json.dumps(bb)
    print json.dumps(query)
    
    elements = collection.find()
    els = []
    for el in elements:
        del el['_id']
        els.append(el)
    response = {
        "type": "FeatureCollection",
        "features":els
    }
    
    return response
    
    
    