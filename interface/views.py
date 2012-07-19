# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings


from django.views.decorators.csrf import csrf_exempt

from broker.models import *

#=======================================================#

def index(request):
    return render_to_response('index.html')


def urls(request):
    return HttpResponse(json.dumps({
        'broker_get_proxies':'',
        'broker_get_map':''
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

def search(request):
    """
    Search pattern
    """
    bb = request.REQUEST.get('bb')
    bb = json.loads(bb)
    query = request.REQUEST.get('q')
    query= json.loads(query)
    cb_data = request.REQUEST.get('cbd')
    cb_queries = request.REQUEST.get('cbq')

    

    proxies = get_for_bb(bb)

    data = []#taManager.query(bb, query)   
    


    response = ""

    response+=cb_data+"("+json.dumps(data)+");"

    for p in proxies:
        p['bb'] = bb
        p['q'] = query
        response+=cb_queries+"("+json.dumps(p)+");"
        #response+=cb_queries+"(\"/"+p['url'] + "/query/"+p['token']+"/"+p['name']+"\");"


    return HttpResponse(response)

def do_search(request):
    query = request.REQUEST.get('q')
    query= json.loads(query)

    maxitems = int(request.REQUEST.get('maxitems','100'))
    offset = int(request.REQUEST.get('offset','0'))
    
    message = {}
    message['token'] = query['token']
    message['message_type'] = "request"
    message['message_format'] = "query"
    message['query'] = {}
    message['query']['BB'] = query['bb']
    message['query']['inventory'] = query['q']
    message['query']['time'] = ""
    message['maxitems'] = maxitems
    message['offset'] = offset

    import urllib2
    url = query['url'] + "/query/" + query['token'] + "/" + query['name'] + "/"

    response = urllib2.urlopen(url, 'remotequery='+json.dumps(message))
    return HttpResponse(response)


def newsearch (request):



	return render_to_response('newsearch.html')
