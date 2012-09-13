# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt

from model_manager.models import *

def index(request):
    return render_to_response('model_index.html')

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

def do_get_model_secondary(models= []):
    fields_table = {
                    'Duct' : {
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
                    'Duct1' : {
                              'name':"Cavidotto Pubblica Illuminazione",
                              'objtype':'LineString',
                              'super':'Duct',
                              'properties':{
                                            'ID' : 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'IDInizio': 'str',
                                            'IDFine': 'str',
                                            'Lunghezza': 'int',
                                            'Tipo': ['Pubblica Illuminazione'],
                                            'Disponibilita': 'str',
                                            'DataCreazione': 'str',
                                            'UltimoAggiornamento': 'str'
                                            }
                              },
                    'Duct2' : {
                              'name':"Cavidotto TLC",
                              'objtype':'LineString',
                              'super':'Duct',
                              'properties':{
                                            'ID' : 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'IDInizio': 'str',
                                            'IDFine': 'str',
                                            'Lunghezza': 'int',
                                            'Tipo': ['Telecomunicazioni'],
                                            'Disponibilita': 'str',
                                            'DataCreazione': 'str',
                                            'UltimoAggiornamento': 'str'
                                            }
                              },
                    'Duct3' : {
                              'name':"Cavidotto Rete Elettrica",
                              'objtype':'LineString',
                              'super':'Duct',
                              'properties':{
                                            'ID' : 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'IDInizio': 'str',
                                            'IDFine': 'str',
                                            'Lunghezza': 'int',
                                            'Type': ['Rete Elettrica'],
                                            'Disponibilita': 'str',
                                            'DataCreazione': 'str',
                                            'UltimoAggiornamento': 'str'
                                            }
                              },
                    'Well' :{
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
                    
                    'Well1' :{
                              'name':"Pozzetto Pubblica Illuminazione",
                              'objtype':'Point',
                              'super':'Well',
                              'properties':{
                                            'ID': 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'Indirizzo': 'str',
                                            'Tipo': ['Pubblica Illuminazione'],
                                            'DataCreazione': 'str',
                                            'UltimoAggiornamento': 'str'
                                            }
                             },
                    
                    'Well2' :{
                              'name':"Pozzetto Telecomunicazioni",
                              'objtype':'Point',
                              'super':'Well',
                              'properties':{
                                            'ID': 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'Indirizzo': 'str',
                                            'Tipo': [ 'Telecomunicazioni'],
                                            'DataCreazione': 'str',
                                            'UltimoAggiornamento': 'str'
                                            }
                             },
                    
                    'Well3' :{
                              'name':"Pozzetto Rete Elettrica",
                              'objtype':'Point',
                              'super':'Well',
                              'properties':{
                                            'ID': 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'Indirizzo': 'str',
                                            'Tipo': ['Rete Elettrica'],
                                            'DataCreazione': 'str',
                                            'UltimoAggiornamento': 'str'
                                            }
                             },
                    
                    'Well4' :{
                              'name':"Pozzetto Fognatura",
                              'objtype':'Point',
                              'super':'Well',
                              'properties':{
                                            'ID': 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'Indirizzo': 'str',
                                            'Tipo': ['Fognatura'],
                                            'DataCreazione': 'str',
                                            'UltimoAggiornamento': 'str'
                                            }
                             },
                    
                    'Well5' :{
                              'name':"Pozzetto Teleriscaldamento",
                              'objtype':'Point',
                              'super':'Well',
                              'properties':{
                                            'ID': 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'Indirizzo': 'str',
                                            'Tipo': ['Teleriscaldamento'],
                                            'DataCreazione': 'str',
                                            'UltimoAggiornamento': 'str'
                                            }
                             },
                    
                    'Well6' :{
                              'name':"Pozzetto Rete Gas",
                              'objtype':'Point',
                              'super':'Well',
                              'properties':{
                                            'ID': 'int',
                                            'Proprietario': ['Lepida S.p.A.', 'IREN'],
                                            'IDProprietario' : 'str',
                                            'Indirizzo': 'str',
                                            'Tipo': ['Rete Gas'],
                                            'DataCreazione': 'str',
                                            'UltimoAggiornamento': 'str'
                                            }
                             },
                    
                    'Tube' :{
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


