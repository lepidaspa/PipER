# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt

from model_manager.models import *



def _get_model(request):
    data = {}
    v = request.REQUEST.get('v', None)
    m = request.REQUEST.get('m', None)
    if v is not None:
        version = DataModelContainer.objects.get(id = v)
    else:
        version = DataModelContainer.objects.order_by('-id')[0]
    for model in version.models:
        if (m is not None and m == model.name) or m is None:
            data[model.name] = {}
            #data[model.name]['_type'] = model.type
            for attribute in model.attributes:
                data[model.name][str(attribute)] = attribute.type
    return HttpResponse(json.dumps(data), mimetype="application/json")
        

def _get_model_secondary(request):
    data = {}
    v = request.REQUEST.get('v', None)
    m = request.REQUEST.get('m', None)
    if v is not None:
        version = DataModelContainer.objects.get(id = v)
    else:
        version = DataModelContainer.objects.order_by('-id')[0]
    for model in version.models:
        if (m is not None and m == model.name) or m is None:
            data[model.name] = {}
            data[model.name]['name'] = model.name
            data[model.name]['objtype'] = model.type
            data[model.name]['properties'] = {}
            for attribute in model.attributes:
                data[model.name]['properties'][str(attribute)] = attribute.type
    return HttpResponse(json.dumps(data), mimetype="application/json")
        
    
    
    
def get_model (request):
    """
    Sends the conversion table
    """

    #fb = settings.FIdER_BACKEND_URL
    #mdl = sendMessageToServer("", fb+"/get_model/last", "GET")

    #fields_table = json.loads(mdl)
    fields_table = {
        'Duct' : {
            '_type':'LineString',
            'ID' : 'int',
            'Owner': 'str',
            'OwnerID' : 'str',
            'StartID': 'str',
            'EndID': 'str',
            'Length': 'int',
            'Type': 'str',
            'Availability': 'str',
            'CreationDate': 'str',
            'LastUpdate': 'str',
        },
        'Well' : {
            '_type':'Point',
            'ID': 'int',
            'Owner': 'str',
            'OwnerID': 'str',
            'Address': 'str',
            'Type': 'str',
            'CreationDate': 'str',
            'LastUpdate': 'str',
        }

    }

    return HttpResponse(json.dumps(fields_table), mimetype="application/json")

def get_model_secondary (request):
    """
    Sends the conversion table
    """

    #fb = settings.FIdER_BACKEND_URL
    #mdl = sendMessageToServer("", fb+"/get_model/last", "GET")

    #fields_table = json.loads(mdl)
    fields_table = {
                    'Duct' : {
                              'name':"Cavidotto",
                              'objtype':'LineString',
                              'properties':{
                                            'ID' : 'int',
                                            'Owner': 'str',
                                            'OwnerID' : 'str',
                                            'StartID': 'str',
                                            'EndID': 'str',
                                            'Length': 'int',
                                            'Type': 'str',
                                            'Availability': 'str',
                                            'CreationDate': 'str',
                                            'LastUpdate': 'str',
                                            }
                              },
                    'Well' :{
                              'name':"Pozzetto",
                              'objtype':'Point',
                              'properties':{
                                            'ID': 'int',
                                            'Owner': 'str',
                                            'OwnerID': 'str',
                                            'Address': 'str',
                                            'Type': 'str',
                                            'CreationDate': 'str',
                                            'LastUpdate': 'str',
                                            }
                             },
                    'Tube' :{
                              'name':"Tubazione",
                              'objtype':'LineString',
                              'properties':{
                                            'ID': 'int',
                                            'Owner': 'str',
                                            'OwnerID': 'str',
                                            'Type': 'str',
                                            'Parent':'Duct'
                                            }
                             },
                    'SpliceEnclosure' :{
                              'name':"Muffola",
                              'objtype':'Point',
                              'properties':{
                                            'ID': 'int',
                                            'Owner': 'str',
                                            'OwnerID': 'str',
                                            'Type': 'str',
                                            'Parent':'Well'
                                            }
                             }
                    
                    }

    return HttpResponse(json.dumps(fields_table), mimetype="application/json")


