from django.http import HttpResponse, HttpResponseRedirect
from broker.models import *
from django.core.management import call_command
from django.conf import settings
try:
    import json
except:
    import simplejson as json
import urllib2
from data.views import *

def index(request):
    return HttpResponse(json.dumps(all_prox()))
    
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

    data = run_query(bb, query)   
    

    response = ""

    response+=cb_data+"("+json.dumps(data)+");"

    for p in proxies:
        p['bb'] = bb
        p['q'] = query
        response+=cb_queries+"("+json.dumps(p)+");"
        #response+=cb_queries+"(\"/"+p['url'] + "/query/"+p['token']+"/"+p['name']+"\");"


    return HttpResponse(response)

def show(request):
    cbd = request.REQUEST.get('cbd', None)
    if cbd is None:
        return HttpResponse()
    jsr = {}
    jsr['type'] = "FeatureCollection"
    jsr['features'] = []
    for meta in Metadata.objects.filter(active=True):
        jf={}
        jf['type']='Feature'
        jf['geometry']={
                        'type':'Polygon', 
                        'coordinates':[
                                       [
                                        [meta.BB_south, meta.BB_east],
                                        [meta.BB_south, meta.BB_west],
                                        [meta.BB_north, meta.BB_west],
                                        [meta.BB_north, meta.BB_east],
                                        [meta.BB_south, meta.BB_east]
                                        ]
                                       ]
                        }
        jf['properties']={
                          "TYPE":"BBOX",
                          'owner':str(meta.proxy.request.owner),
                          "highlight":"false"
        }
        jsr['features'].append(jf)
        
    return HttpResponse(cbd+"("+json.dumps(jsr)+");")
        

def do_search(request):
    query = request.REQUEST.get('q')
    query= json.loads(query)

    maxitems = int(request.REQUEST.get('maxitems','10000'))
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

def toggle(request, id):
    m = Metadata.objects.get(id=id)
    m.active = not m.active
    m.save()
    
    return HttpResponseRedirect('/broker')
    
def force_refresh(request):
    return HttpResponse(force_refresh_response())

def force_refresh_response():
    yield "<div>starting</div>"
    for proxy in Proxy.objects.all():
        try:
            call_command('pull_remote', str(proxy.id))
            yield "<div>pulled proxy %s</div>" % str(proxy.id)
        except:
            yield "<div>error pulling proxy %s</div>" % str(proxy.id)
        try:
            call_command('get_remote', str(proxy.id))
            yield "<div>got proxy %s</div>" % str(proxy.id)
        except:
            yield "<div>error getting proxy %s</div>" % str(proxy.id)
    yield "<div>done</div>"


def force_pull_remote(request):
    proxy = request.REQUEST.get('id', None)
    return HttpResponse(force_pull_remote_response())

def force_pull_remote_response(proxy):
    yield "<div>starting</div>"
    if proxy is None:
        for proxy in Proxy.objects.all():
            try:
                yield "<div>pulling proxy %s</div>" % str(proxy.id)
                call_command('pull_remote', str(proxy.id))
                yield "<div>pulled proxy %s</div>" % str(proxy.id)
            except:
                yield "<div>error pulling proxy %s</div>" % str(proxy.id)
        yield "<div>done</div>"
    else:
        yield "<div>getting proxy %s</div>" % str(proxy)
        call_command('pull_remote', str(proxy))
        yield "<div>got proxy %s</div>" % str(proxy)
    

def force_get_remote(request):
    proxy = request.REQUEST.get('id', None)
    return HttpResponse(force_pull_remote_response(proxy))

def force_get_remote_response(proxy):
    yield "<div>starting</div>"
    if proxy is None:
        for proxy in Proxy.objects.all():
            try:
                yield "<div>getting proxy %s</div>" % str(proxy.id)
                call_command('get_remote', str(proxy.id))
                yield "<div>got proxy %s</div>" % str(proxy.id)
            except:
                yield "<div>error getting proxy %s</div>" % str(proxy.id)
        yield "<div>done</div>"
    else:
        yield "<div>getting proxy %s</div>" % str(proxy)
        call_command('get_remote', str(proxy))
        yield "<div>got proxy %s</div>" % str(proxy)
        
        


def clear_db(request):
    tok = request.REQUEST.get('token')
    meta = request.REQUEST.get('meta')
    return HttpResponse(clear_db_response(tok,meta))

def clear_db_response(token=None, metadata=None):
    yield "starting clear"
    call_command('clear_db', token, metadata)
    yield "cleared"



    
def all_owners(request):
    return HttpResponse(json.dumps([o.name for o in Owner.objects.all()]))
    
def delete(request, proxy_id):
    ProxyRequest.objects.get(token = proxy_id).delete()
    return HttpResponse()
    