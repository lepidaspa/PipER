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

def do_get_model_secondaty(models= []):
    fields_table = {
                    'Duct' : {
                              'name':"Cavidotto",
                              'objtype':'LineString',
                              'super':'Duct',
                              'properties':{
                                            'ID' : 'int',
                                            'Owner': 'str',
                                            'OwnerID' : 'str',
                                            'StartID': 'str',
                                            'EndID': 'str',
                                            'Length': 'int',
                                            'Type': ['Pubblica Illuminazione', 'TLC', 'Rete Elettrica'],
                                            'Availability': 'str',
                                            'CreationDate': 'str',
                                            'LastUpdate': 'str',
                                            }
                              },
                    'Duct1' : {
                              'name':"Cavidotto Pubblica Illuminazione",
                              'objtype':'LineString',
                              'super':'Duct',
                              'properties':{
                                            'ID' : 'int',
                                            'Owner': 'str',
                                            'OwnerID' : 'str',
                                            'StartID': 'str',
                                            'EndID': 'str',
                                            'Length': 'int',
                                            'Type': ['Pubblica Illuminazione'],
                                            'Availability': 'str',
                                            'CreationDate': 'str',
                                            'LastUpdate': 'str',
                                            }
                              },
                    'Duct2' : {
                              'name':"Cavidotto TLC",
                              'objtype':'LineString',
                              'super':'Duct',
                              'properties':{
                                            'ID' : 'int',
                                            'Owner': 'str',
                                            'OwnerID' : 'str',
                                            'StartID': 'str',
                                            'EndID': 'str',
                                            'Length': 'int',
                                            'Type': ['TLC'],
                                            'Availability': 'str',
                                            'CreationDate': 'str',
                                            'LastUpdate': 'str',
                                            }
                              },
                    'Duct3' : {
                              'name':"Cavidotto Rete Elettrica",
                              'objtype':'LineString',
                              'super':'Duct',
                              'properties':{
                                            'ID' : 'int',
                                            'Owner': 'str',
                                            'OwnerID' : 'str',
                                            'StartID': 'str',
                                            'EndID': 'str',
                                            'Length': 'int',
                                            'Type': ['Rete Elettrica'],
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
                              'container':'Duct',
                              'properties':{
                                            'ID': 'int',
                                            'Owner': 'str',
                                            'OwnerID': 'str',
                                            'Type': 'str',
                                            }
                             },
                    'SpliceEnclosure' :{
                              'name':"Muffola",
                              'objtype':'Point',
                              'container':'Well',
                              'properties':{
                                            'ID': 'int',
                                            'Owner': 'str',
                                            'OwnerID': 'str',
                                            'Type': 'str',
                                            'Parent':'Well'
                                            }
                             }
                    
                    }
    
    if len(models) == 0 :
        return fields_table
    else:
        ff = {}
        for m in models:
            ff[m] = fields_table[m]
        return ff

def get_model_secondary (request):
    """
    Sends the conversion table
    """
    
    models = request.REQUEST.get('models', [])
    if models is not None:
        models = models.split('|')
    
    fields_table = do_get_model_secondary(models)
   

    return HttpResponse(json.dumps(fields_table), mimetype="application/json")


