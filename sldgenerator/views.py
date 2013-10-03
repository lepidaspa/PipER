# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt

from model_manager.views import *

import sld

def get_default_sld(request):
    color_list = [
                  '#FF7A00',
                  '#F900FF',
                  '#05FF00',
                  '#0085FF',
                  '#FFCE00',
                  '#0085FF',
                  '#00FFF9',
                  '#64FE2E',
                  '#00ff00',
                  '#ffff00',
                  '#0005FF',
                  '#0000a0',
                  '#0000ff',
                  '#00ffff',
                  '#ff0000'
                  ]
    
    m = "Cavidotto"
    f = "Tipo"
    
    mod = inner_get_model()
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
    for v in fv:
        
        color = color_list[i]
        i = i+1
        
        default_feature_type_style = default_style.create_featuretypestyle()
        
        default_feature_type_style_rule = default_feature_type_style.create_rule(f+"__"+v)
        default_feature_type_style_rule.create_symbolizer("Line")
        #RULE
        dftsrf = default_feature_type_style_rule.create_filter(f, '==', v)
        #SYMBOL
        dftsym = default_feature_type_style_rule.LineSymbolizer
        dftstroke = dftsym.create_stroke()
        dftstroke.create_cssparameter("stroke",color)
        dftstroke.create_cssparameter("stroke-width","2")
        
        dftsymp  = default_feature_type_style_rule.PointSymbolizer
        dgftpoint = dftsymp.Graphic
        dgftpoint.Size = "10"
        dmgftpoint = dgftpoint.Mark
        dmgftpoint.WellKnownName="circle"
        dmgftpoint.create_stroke()
        dsmgftpoint = dmgftpoint.Stroke
        dsmgftpoint.create_cssparameter('stroke', color)
        dsmgftpoint.create_cssparameter("stroke-width","2")
        
        #dmgftpoint.create_fill()
        dfmgftpoint = dmgftpoint.Fill
        dfmgftpoint.CssParameters[0].Value = color
        dfmgftpoint.create_cssparameter('fill-opacity', "0.1")   
    return HttpResponse(sf.as_sld(), mimetype="text/xml")
      
def get_selected_sld(request):
    color_list = [
                  '#FF7A00',
                  '#F900FF',
                  '#05FF00',
                  '#0085FF',
                  '#FFCE00',
                  '#0085FF',
                  '#00FFF9',
                  '#64FE2E',
                  '#00ff00',
                  '#ffff00',
                  '#0005FF',
                  '#0000a0',
                  '#0000ff',
                  '#00ffff',
                  '#ff0000'
                  ]
    
    m = "Cavidotto"
    f = "Tipo"
    
    mod = inner_get_model_secondary()
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
    nl = sf.create_namedlayer("selected_elements")
    slected_style = nl.create_userstyle()
    slected_style.Title="default"
    for v in fv:
        color = color_list[i]
        i = i+1
        slected_feature_type_style = slected_style.create_featuretypestyle()
        
        slected_feature_type_style_rule = slected_feature_type_style.create_rule(f+"__"+v)
        slected_feature_type_style_rule.create_symbolizer("Line")
        #RULE
        sftsrf = slected_feature_type_style_rule.create_filter(f, '==', v)
        #SYMBOL
        
        
        sftsym = slected_feature_type_style_rule.LineSymbolizer
        sftstroke = sftsym.create_stroke()
        sftstroke.create_cssparameter("stroke",color)
        sftstroke.create_cssparameter("stroke-width","5")
        
        
        sftsymp  = slected_feature_type_style_rule.PointSymbolizer
        sgftpoint = sftsymp.Graphic
        sgftpoint.Size = "15"
        smgftpoint = sgftpoint.Mark
        smgftpoint.WellKnownName="circle"
        smgftpoint.create_stroke()
        ssmgftpoint = smgftpoint.Stroke
        ssmgftpoint.create_cssparameter('stroke', color)
        ssmgftpoint.create_cssparameter("stroke-width","5")
        
        #dmgftpoint.create_fill()
        sfmgftpoint = smgftpoint.Fill
        sfmgftpoint.CssParameters[0].Value = color
        sfmgftpoint.create_cssparameter('fill-opacity', "0.2")   
    return HttpResponse(sf.as_sld(), mimetype="text/xml")


