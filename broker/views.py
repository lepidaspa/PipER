from django.http import HttpResponse
from broker.models import *

from django.conf import settings
try:
    import json
except:
    import simplejson as json
import urllib2



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
    url = query['url'] + "query/" + query['token'] + "/" + query['name'] + "/"

    response = urllib2.urlopen(url, 'remotequery='+json.dumps(message))
    return HttpResponse(response)
