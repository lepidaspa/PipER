# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt

from model_manager.views import *

import sld

def get_sld(request):
    
    m = request.REQUEST.get('model', "TEST")
    f = request.REQUEST.get('field', "ANY")
    
    sf = sld.StyledLayerDescriptor()
    
    nl = sf.create_namedlayer(m)
    ustyle = nl.create_userstyle()
    ftstyle = ustyle.create_featuretypestyle()
    ftsr = ftstyle.create_rule()
    ftsr.create_filter(f, '=', '10')
    
    return HttpResponse(sf.as_sld())
    

