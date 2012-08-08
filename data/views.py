# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt

import pymongo

from django.contrib.gis.gdal import OGRGeometry
from pymongo import Connection, GEO2D


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
    
    db.elements.create_index([('_center.coordinates',GEO2D)])
    
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
    poly = [[bb[0], bb[1]],[bb[2], bb[1]],[bb[2], bb[3]],[bb[0], bb[3]],[bb[0], bb[1]]]
    print json.dumps(poly)
    elements = collection.find({ "_center.coordinates" : { "$within" : { "$polygon" : poly } } })
    els = []
    for el in elements:
        del el['_id']
        els.append(el)
    response = {
        "type": "FeatureCollection",
        "features":els
    }
    
    return response
    
    
    