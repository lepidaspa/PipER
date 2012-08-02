# Create your views here.
import json
import urllib2 
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

from broker.models import * 
from django.views.decorators.csrf import csrf_exempt


#=======================================================#

def index(request):
    return render_to_response('index.html')


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

        
        url = path

        if request.method == 'GET':
                url_ending = '%s?%s' % (url, request.GET.urlencode())
                url = "http://" + url_ending
                response, content = conn.request(url, request.method)
        elif request.method == 'POST':
                url = "http://" + url
                data = request.POST.urlencode()
                response, content = conn.request(url, request.method, data)
        return HttpResponse(content, status = int(response['status']), mimetype = response['content-type'])