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
    default_style = nl.create_userstyle()
    default_style.Title="default"
    slected_style = nl.create_userstyle()
    slected_style.Title="selected"
    for v in fv:
        
        color = color_list[i]
        i = i+1
        
        default_feature_type_style = default_style.create_featuretypestyle()
        slected_feature_type_style = slected_style.create_featuretypestyle()
        
        default_feature_type_style_rule = default_feature_type_style.create_rule(f+"__"+v)
        slected_feature_type_style_rule = slected_feature_type_style.create_rule(f+"__"+v)
        default_feature_type_style_rule.create_symbolizer("Line")
        slected_feature_type_style_rule.create_symbolizer("Line")
        #RULE
        ftsrf = default_feature_type_style_rule.create_filter(f, '==', v)
        #SYMBOL
        dftsym = default_feature_type_style_rule.LineSymbolizer
        dftstroke = dftsym.create_stroke()
        dftstroke.create_cssparameter("stroke",color)
        dftstroke.create_cssparameter("stroke-width","2")
        
        
        sftsym = slected_feature_type_style_rule.LineSymbolizer
        sftstroke = sftsym.create_stroke()
        sftstroke.create_cssparameter("stroke",color)
        sftstroke.create_cssparameter("stroke-width","4")
        
        dftsymp  = default_feature_type_style_rule.PointSymbolizer
        dgftpoint = dftsymp.Graphic
        dgftpoint.Size = "6"
        dmgftpoint = dgftpoint.Mark
        dmgftpoint.WellKnownName="circle"
        dmgftpoint.create_stroke()
        dsmgftpoint = dmgftpoint.Stroke
        dsmgftpoint.create_cssparameter('stroke', color)
        dsmgftpoint.create_cssparameter("stroke-width","2")
        
        #dmgftpoint.create_fill()
        dfmgftpoint = dmgftpoint.Fill
        dfmgftpoint.create_cssparameter('fill', color)
        dfmgftpoint.create_cssparameter('fill-opacity', "0.1")   
        
        
        sftsymp  = slected_feature_type_style_rule.PointSymbolizer
        sgftpoint = sftsymp.Graphic
        sgftpoint.Size = "6"
        smgftpoint = sgftpoint.Mark
        smgftpoint.WellKnownName="circle"
        smgftpoint.create_stroke()
        ssmgftpoint = smgftpoint.Stroke
        ssmgftpoint.create_cssparameter('stroke', color)
        ssmgftpoint.create_cssparameter("stroke-width","4")
        
        #dmgftpoint.create_fill()
        sfmgftpoint = smgftpoint.Fill
        sfmgftpoint.create_cssparameter('fill', color)
        sfmgftpoint.create_cssparameter('fill-opacity', "0.1")   


    return HttpResponse(sf.as_sld())


