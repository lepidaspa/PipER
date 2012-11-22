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


def put_data(proxy, data):
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
    db.elements.create_index('_metadata')
    
    #do coorections on data wwith specific elements...
    #avoid duplicates
    
    for metadata_name, featurecollection in data['data']['upserts'].items():
        for fc in featurecollection:
            for feature in fc['features']:
                print feature['properties']
                polygon = OGRGeometry(json.dumps(feature['geometry']))
                feature['_center'] = json.loads(polygon.geos.centroid.json)
                feature['_proxy'] = token_id
                feature['properties']['_proxy'] = token_id
                feature['_metadata'] = metadata_name
                feature['properties']['_metadata'] = metadata_name
                feature['properties']['Fornitore']=proxy.request.owner.name
                feature['properties']['_baseurl']=proxy.request.url
                collection.insert(feature)
    return

def clear_db(token=None, metadata=None):
    connection = Connection()
    db = connection.data
        
    if token is None and metadata is None:
        db.elements.drop()
    elif token is not None and metadata is not None:
        collection = db['elements']
        collection.remove({'_token':token, '_metadata':metadata})
    return 
            
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
        el['properties']['IDPiper'] = str(el['_id'])
        del el['_id']
        els.append(el)
    response = {
        "type": "FeatureCollection",
        "features":els
    }
    
    return response
    
    
    