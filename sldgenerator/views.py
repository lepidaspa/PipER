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
    
    m = request.REQUEST.get('model', "Duct")
    f = request.REQUEST.get('field', "Tipo")
    
    mod = do_get_model_secondary([m])
    print json.dumps(mod)
    
    if mod =={}:
        print "no model"
        return HttpResponse("ERROR")
    
    props = mod[m]['properties']
    if not props.has_key(f):
        
        print "no prop"
        return HttpResponse("ERROR")
    
    fv = props[f]
    
    if not isinstance(fv, type([])):
        
        print "no instances"
        return HttpResponse("ERROR")
    
    ot = mod[m]['objtype']
    if ot == "LineString":
        ot = sld.LineSymbolizer
    elif ot == "Point":
        ot = sld.PointSymbolizer
    
    
    sf = sld.StyledLayerDescriptor()
    
    nl = sf.create_namedlayer(m)
    ustyle = nl.create_userstyle()
    for v in fv:
        ftstyle = ustyle.create_featuretypestyle()
        ftsr = ftstyle.create_rule(f+"__"+v, ot)
        ftsrf = ftsr.create_filter(f, '==', v)
        
    return HttpResponse(sf.as_sld())
    

