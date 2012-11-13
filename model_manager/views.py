# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt

from model_manager.models import *
from broker.models import *

def index(request):
    return render_to_response('model_index.html')

def _get_model(request):
    data = {}
    m = request.REQUEST.get('m', None)
    for model in DataModel.objects.all():
        if (m is not None and m == model.name) or m is None:
            data[model.name] = {}
            #data[model.name]['_type'] = model.type
            for attribute in model.attributes.all():
                data[model.name][str(attribute)] = attribute.type
    return HttpResponse(json.dumps(data), mimetype="application/json")
        

def _get_model_secondary(request):
    data = {}
    m = request.REQUEST.get('m', None)
    for model in DataModel.objects.all():
        if (m is not None and m == model.name) or m is None:
            data[model.name] = {}
            data[model.name]['name'] = model.name
            data[model.name]['objtype'] = model.geo_type
            data[model.name]['federated'] = model.federated 
            
            data[model.name]['super'] = model.container.name if model.container is not None else model.name 
            if model.within is not None:
                data[model.name]['container'] = model.within.name
                
            data[model.name]['properties'] = {}
            for attribute in model.attributes.all():
                if attribute.type == 'owner':
                    data[model.name]['properties'][str(attribute)] = [ str(o) for o in Owner.objects.all()]
                elif attribute.type == 'infrastructure':
                    data[model.name]['properties'][str(attribute)] = [ str(o) for o in Infrastructure.objects.all()]
                else:
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

def do_get_model_secondary(models= []):
    fields_table = {
                    'Duct' : {
                              'federated':True,
                              'name':"Cavidotto",
                              'objtype':'LineString',
                              'super':'Duct',
                              'properties':{
                                            'ID' : 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'IDInizio': 'str',
                                            'IDFine': 'str',
                                            'Lunghezza': 'int',
                                            'Tipo': ['Pubblica Illuminazione', 'Telecomunicazioni', 'Rete Elettrica', 'Fognatura', 'Teleriscaldamento', 'Rete Gas'],
                                            'Disponibilita': 'str',
                                            'DataCreazione': 'str',
                                            'UltimoAggiornamento': 'str'
                                            }
                              },
                    'Well' :{
                              'federated':True,
                              'name':"Pozzetto",
                              'objtype':'Point',
                              'super':'Well',
                              'properties':{
                                            'ID': 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'Indirizzo': 'str',
                                            'Tipo': ['Pubblica Illuminazione', 'Telecomunicazioni', 'Rete Elettrica', 'Fognatura', 'Teleriscaldamento', 'Rete Gas'],
                                            'DataCreazione': 'str',
                                            'UltimoAggiornamento': 'str'
                                            }
                             },
                    
                    'Tube' :{
                              'federated':False,
                              'name':"Tubazione",
                              'objtype':'LineString',
                              'container':'Duct',
                              'super':'Tube',
                              'properties':{
                                            'ID': 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'Tipo': ['Telecomunicazioni'],
                                            'Contenitore':'Tube',
                                            }
                             },
                    'SpliceEnclosure' :{
                              'federated':False,
                              'name':"Muffola",
                              'objtype':'Point',
                              'container':'Well',
                              'super':'SpliceEnclosure',
                              'properties':{
                                            'ID': 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'Tipo': ['Telecomunicazioni'],
                                            'Contenitore':'Well',
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
    if models != []:
        models = models.split('|')
    
    fields_table = do_get_model_secondary(models)
    
    return HttpResponse(json.dumps(fields_table), mimetype="application/json")


