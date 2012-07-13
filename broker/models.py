from django.db import models
from django.db.models import Q
# Create your models here.
import json

def startup(url, tok):
    p = ProxyRequest()
    p.url = url
    p.token = tok
    p.save()

def save_meta(metadata):
    tok = metadata['token']
    try:
        pr = ProxyRequest.objects.get(token = tok)
    except:
        return False
    p = Proxy()
    p.request = pr
    p.manifest = metadata
    p.mode_read = metadata['operations']['read'] if metadata['operations']['read'] != "none" else None
    p.mode_write = metadata['operations']['write'] if metadata['operations']['write'] != "none" else None
    p.mode_query = json.dumps(metadata['operations']['query']) if metadata['operations']['query'] != "none" else None
    p.save()

    for md in metadata['metadata']:
        mm = Metadata()
        mm.proxy = p
        mm.meta = json.dumps(md)
        mm.BB_south = md['area'][0]
        mm.BB_east = md['area'][1]
        mm.BB_north = md['area'][2]
        mm.BB_west = md['area'][3] 
        mm.name = md['name']
        mm.save()
    
    return True	

def get_for_bb(BB):
        w = BB[0]
        s = BB[1]
        e = BB[2]
        n = BB[3]

        #BB_east > BB_west
        #BB_north > BB_south

        q_in = Q()

        wle = Q(BB_west__lt = e)
        wlw = Q(BB_west__lt = w)
        ege = Q(BB_east__gt = e)
        egw = Q(BB_east__gt = w)
        sls = Q(BB_south__lt = s)
        sln = Q(BB_south__lt = n)
        ngs = Q(BB_north__gt = s)
        ngn = Q(BB_north__gt = n)

        se_in = Q(wle, ege, sls, ngs)
        ne_in = Q(wle, ege, sln, ngn)
        sw_in = Q(wlw, egw, sls, ngs)
        nw_in = Q(wlw, egw, sln, ngn)

        q_in.add(se_in, Q.OR)
        q_in.add(ne_in, Q.OR)
        q_in.add(nw_in, Q.OR)
        q_in.add(sw_in, Q.OR)


        mdata = Metadata.objects.filter(q_in, proxy__mode_query__isnull=False)

        # prs = ProxyRequest.objects.filter(data__in= Proxy.objects.filter(mode_query__isnull=False, metadata__name__in=mdata).distinct()).distinct()
        mdata = Metadata.objects.all()
	data = []
        for meta in mdata: 
            data.append({'url':meta.proxy.request.url, 'token':meta.proxy.request.token, 'name':meta.name})
        return data 
                

class ProxyRequest(models.Model):
    url = models.URLField()
    token = models.TextField(unique=True, primary_key=True, db_index=True)
    def __str__(self):
        return self.token

class Proxy(models.Model):
    request = models.OneToOneField(ProxyRequest, related_name="data")
    manifest = models.TextField()
    mode_read = models.TextField(null=True, blank=True)
    mode_write = models.TextField(null=True, blank=True)
    mode_query = models.TextField(null=True, blank=True)
    
        
class Metadata(models.Model):
    proxy = models.ForeignKey(Proxy, related_name="metadata")
    BB_north = models.FloatField()
    BB_east = models.FloatField()
    BB_south = models.FloatField()
    BB_west = models.FloatField()
    meta = models.TextField()
   
    name = models.TextField()
