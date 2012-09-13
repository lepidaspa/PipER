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
    color_list = [
                  '#ffa500',
                  '#800000',
                  '#008000',
                  '#808000',
                  '#000000',
                  '#808080',
                  '#c0c0c0',
                  '#ff00ff',
                  '#00ff00',
                  '#ffff00',
                  '#add8e6',
                  '#0000a0',
                  '#0000ff',
                  '#00ffff',
                  '#ff0000'
                  ]
    
    m = "Duct"
    f = "Tipo"
    
    mod = do_get_model_secondary([m])
    print json.dumps(mod)
    
    if mod =={}:
        print "no model"
        #return HttpResponse("ERROR")
    
    props = mod[m]['properties']
    if not props.has_key(f):
        
        print "no prop"
        #return HttpResponse("ERROR")
    
    fv = props[f]
    
    if not isinstance(fv, type([])):
        
        print "no instances"
        #return HttpResponse("ERROR")
    
    ot = mod[m]['objtype']
    if ot == "LineString":
        ot = "Line"
    elif ot == "Point":
        ot = "Point"
    
    i = 0
    
    sf = sld.StyledLayerDescriptor()
    
    nl = sf.create_namedlayer("elements")
    ustyle = nl.create_userstyle()
    for v in fv:
        
        color = color_list[i]
        i = i+1
        
        ftstyle = ustyle.create_featuretypestyle()
        ftsr = ftstyle.create_rule(f+"__"+v)
        #RULE
        ftsrf = ftsr.create_filter(f, '==', v)
        #SYMBOL
        ftsym  = ftsr.create_symbolizer("Line")
        ftstroke = ftsym.create_stroke()
        ftstroke.create_cssparameter("stroke",color)
        ftstroke.create_cssparameter("stroke-width","2")
        
        ftsymp  = ftsr.PointSymbolizer
        gftpoint = sld.Graphic(ftsymp)
        gftpoint.Size = "6"
        mgftpoint = sld.Mark(gftpoint)
        mgftpoint.WellKnownName="circle"
        smgftpoint = mgftpoint.Stroke
        smgftpoint.create_cssparameter('stroke', color)
        
        fmgftpoint = mgftpoit.Fill
        fmgftpoint.create_cssparameter('fill', color)
        fmgftpoint.create_cssparameter('fill-opacity', "0.1")   


    return HttpResponse(sf.as_sld())


