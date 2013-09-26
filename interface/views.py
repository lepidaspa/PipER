# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
import sys
from broker.models import * 
from django.views.decorators.csrf import csrf_exempt
from uuid import  uuid4

import subprocess 
import os
#=======================================================#

def index(request):
    return render_to_response('index.html')

def export(request):
    filter = request.REQUEST.get('f')
    selected = request.REQUEST.get('s')
    bb= json.loads(request.REQUEST.get('b'))
    pois = request.REQUEST.get('p')
    bl = request.REQUEST.get('l')
    
    return render_to_response('export.html', {
        'bb':{
              't':bb[3],
              'l':bb[0],
              'r':bb[2],
              'b':bb[1]
              },
        'filter':filter,
        'selected':selected,
        'pois': pois,
        'bl':bl
    })

def do_export(request):
    filter = request.REQUEST.get('f')
    selected = request.REQUEST.get('s')
    bb= request.REQUEST.get('b')
    pois = request.REQUEST.get('p')
    bl = request.REQUEST.get('l')
    
    w = request.REQUEST.get('w')
    h = request.REQUEST.get('h')
    
    url = "http://5.144.184.145/export?f="+filter+"&s="+selected + "&b=" + bb + "&p=" + pois + "&l=" + bl
    filename = "/tmp/"+str(uuid4())+".png"
    filename = filename.replace('-','')
   
    p = subprocess.call(['phantomjs', '/home/ubuntu/PipER/export.js', url, filename])
    f = open(filename)
    c = f.read()
    f.close()
    os.remove(filename)
    return HttpResponse(c, mimetype="image/png")

def urls(request):
    return HttpResponse(json.dumps({
        'broker_get_proxies':'',
        'broker_get_map':'',
        'get_model':"/request/getmodel"
    }))
    


#=======================================================#

def get_model (request):
    """
    Sends the conversion table
    """

    #fb = settings.FIdER_BACKEND_URL
    #mdl = sendMessageToServer("", fb+"/get_model/last", "GET")

    #fields_table = json.loads(mdl)
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

@csrf_exempt
def start_token (request):
    """
    Answers the registration request and sends the "unique" token
    """


    #fb = settings.get('FIdER_BACKEND_URL', "")
    #mdl = sendMessageToServer("", fb+"/get_model/last", "GET")
    
    #v = json.loads(mdl)
    #v = v['version']

    url =  request.REQUEST.get('from')

    v = 1
 
    import uuid
    token = str(uuid.uuid4()).replace('-','_')
    #TODO: prepare token and session
    welcome_message = {
        "token": token,
        "message_type": u'response',
        "message_format": u'welcome',
        "latest_model_version": v,
    }

    startup(url, token)

    return HttpResponse(json.dumps(welcome_message), mimetype="application/json")

@csrf_exempt
def approve_manifest (request):
    """
    Approves the manifest and confirms the creation of the softproxy on the main server
    """
    print request.REQUEST.get('from',"CAZZI")
    print "Answering manifest request"

    message = json.loads(request.body)
    approval = save_meta(message) #save to server     

    manifestapproval = {
        "message_type" : u'response',
        "message_format" : u'manifest',
        "approved": approval,
        "message": "Manifest approved" if approval else "Manifest Not Approved"
    }


    print message

    return HttpResponse(json.dumps(manifestapproval), mimetype="application/json")

def request_write (request):
    """
    Answers a write request message
    """
    jsonmessage = json.loads(request.REQUEST.get('jsondata', None))
    writes = jsonmessage['data']['upsert'].keys()
    response_write = {
        "token": jsonmessage['token'],
        "message_type": u'response',
        "message_format": u'write',
        "acknowledge": {
            "upsert": writes,
            "delete": []
        },
        "anomalies": []
    }

    return HttpResponse(json.dumps(response_write), mimetype="application/json")



def sendMessageToServer (jsonmessage, url, method):
    """
    Sends a json message to the main server and returns success if the response code is correct
    :param jsonmessage: data to be sent to the server, already in json format (json.dumps())
    :param url:
    :param method:
    :return: response from server
    """


    #TODO: placeholder, implement, note that cannot be async if we want to keep the full comm cycle in this one only; should we also keep the full response from the other server?

    datalen = len(jsonmessage)
    headers = {'Content-Type': 'application/json', 'Content-Length': datalen}

    req = urllib2.Request(url, jsonmessage, headers)
    conn = urllib2.urlopen(req)

    return conn.read()


def proxy(request, path):
        import httplib2
        conn = httplib2.Http()

        ssl = False
        
        url = path
        limit = 7
        if(url[0:4] == "http" and url[6] == "/"):
            if(url[4] == "s"):
                ssl = True
                limit = 8
            url = url[limit:]
                

        if request.method == 'GET':
                url_ending = '%s?%s' % (url, request.GET.urlencode())
                url_begin = "http://" if not ssl else "https://" 
                url = url_begin + url_ending
                response, content = conn.request(url, request.method)
        elif request.method == 'POST':
                url_begin = "http://" if not ssl else "https://" 
                url = url_begin + url
                data = request.POST.urlencode()
                response, content = conn.request(url, request.method, data)
        return HttpResponse(content, status = int(response['status']), mimetype = response['content-type'])
    
import urllib
    
@csrf_exempt
def download_static_map (request, **kwargs):
    """
    Downloads a static background map from an external service
    :param request:
    :param kwargs:
    :return:
    """

    print "Downloading static map from request"


    """
    proxy_id = kwargs['proxy_id']
    meta_id = kwargs['meta_id']
    map_id = kwargs['map_id']

    proxy_type = proxy_core.learnProxyTypeAdv(proxy_id,
proxy_core.getManifest(proxy_id))

    # getting the maps from the gj dir (or ST in case of the standalone
instance)
    if proxy_type != 'local':
        pathtojs = os.path.join (proxyconf.baseproxypath, proxy_id,
proxyconf.path_geojson, meta_id, map_id)
    else:
        pathtojs = os.path.join (proxyconf.baseproxypath, proxy_id,
proxyconf.path_standalone, map_id)

    mapdataraw = json.load(open(pathtojs))

    mapinfo = proxy_core.getMapFileStats(pathtojs)

    print "Working on map data for %s/%s/%s:\n%s" % (proxy_id, meta_id,
map_id, mapinfo)
    """

    try:
        print "Received parameters array, going by POST data"
        #print request.REQUEST
        params = request.REQUEST.get('jsondata', None)
        print params
        params = json.loads(params)
        
    except Exception as ex:
        print "Missing parameters array, going by default"
        params = None

    print "Params: %s" % params.items()

    urlparams = {}
    urlparams['provider'] = params['provider']

    if params['provider'] == 'google':
        baseurl = "http://maps.googleapis.com/maps/api/staticmap"
        urlparams['format'] = 'png32'
        sizeX = min(params['drawsize'][0], 640)
        sizeY = min(params['drawsize'][1], 640)
        urlparams['size']= str(sizeX)+'x'+str(sizeY)
        # note: could use 2 as scale but creates issues later on the js side
        urlparams['scale']='1'
        urlparams['sensor']='false'
        try:
            urlparams['maptype'] = params['maptype']
            print "Maptype from client params: %s" % params['maptype']
        except:
            print "Non valid maptype from client params: %s" % params['maptype']
            urlparams['maptype'] = 'roadmap'

    if params['provider'] == 'osm':
        sizeX = min(params['drawsize'][0], 1280)
        sizeY = min(params['drawsize'][1], 1280)
        urlparams['size']= str(sizeX)+'x'+str(sizeY)
        baseurl = "http://staticmap.openstreetmap.de/staticmap.php"
        try:
            urlparams['maptype'] = params['maptype']
            print "Maptype from client params: %s" % params['maptype']
        except:
            urlparams['maptype'] = 'mapnik'

    print "Partially compiled: %s" % urlparams

    print "Created render defaults for %s.%s" % (urlparams['provider'],urlparams['maptype'])

    print params['drawcenter']

    urlparams['center'] = str(params['drawcenter'][0])+","+str(params['drawcenter'][1])
    urlparams['zoom'] = params['drawzoom']

    """
    try:
        urlparams['center'] = params['center']
    except:
        centerY = str((mapinfo['bbox'][1]+mapinfo['bbox'][3])/2)
        centerX = str((mapinfo['bbox'][2]+mapinfo['bbox'][4])/2)
        urlparams['center'] = "%s,%s" % (centerY,centerX)
    """


#http://maps.googleapis.com/maps/api/staticmap?size=640x640&scale=2&maptype=roadmap&visible=44.2506162174,12.3382646288|44.2667622346,12.3572303763&sensor=false

#http://staticmap.openstreetmap.de/staticmap.php?center=40.714728,-73.998672&zoom=14&size=865x512&maptype=mapnik

    print "URL params %s" % urlparams


    params_serialized = []
    for key, value in urlparams.items():
        params_serialized.append((key, value))

    paramsencoded = urllib.urlencode (params_serialized)
    print "Encoded: %s" % baseurl+"?"+paramsencoded

    try:
        outimage = urllib2.urlopen(baseurl+"?"+paramsencoded).read()
        outimagestr = outimage.encode("base64")
        #print outimage
    except Exception as ex:
        print "ERROR: %s " % ex
        traceback.print_exc()
        raise

    return HttpResponse(outimagestr)
