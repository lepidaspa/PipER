# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt

from model_manager.models import *

import sld

def get_sld(request):
    sf = sld.StyledLayerDescriptor()
    
    return HttpResponse(sf.as_sld())
    

