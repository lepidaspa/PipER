# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt

from model_manager.models import *



def get_models(request):
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
    return HttpResponse(json.dumps(data))
        
    