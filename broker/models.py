from django.db import models
from django.db.models import Q
from django.contrib.auth.models import Group
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
    try:
        print "adding "+metadata['provider']
        ow = Owner.objects.get(name=metadata['provider'])
    except:
        print "new "+metadata['provider']
        try:
            ow = Owner()
            ow.name = metadata['provider']
            g = Group()
            g.name = metadata['provider']
            g.save()
            ow.group = g
            ow.save()
        except:
            pass
    p = Proxy()
    p.request = pr
    pr.owner = ow
    pr.save()
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
        
    rt = MetadataRefreshTime()
    rt.metadata = p
    rt.save()
    
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

        from django.db import connection
        print connection.queries

        #prs = ProxyRequest.objects.filter(data__in= Proxy.objects.filter(mode_query__isnull=False, metadata__name__in=mdata).distinct()).distinct()
        mdata = Metadata.objects.all().exclude(proxy__mode_query__contains="""{"time": "none", "inventory": "none", "geographic": "none", "bi": "none", "signs": false}""")
        data = []
        for meta in mdata: 
            data.append({
                         'url':meta.proxy.request.url, 
                         'token':meta.proxy.request.token, 
                         'name':meta.name
                         })
        return data 
    
def all_prox():
    ret = []
    for owner in Owner.objects.all():
        oj = {}
        oj['name']=owner.name
        oj['data_count'] = owner.proxies.count()
        oj['global_count'] = 0
        oj['data'] = []
        for proxy in owner.proxies.all():
            pj = {}
            pj['token']=proxy.token
            pj['url']=proxy.url
            pj['manifest']=proxy.data.manifest
            pj['token']=proxy.token
            
            pj['meta_count']=proxy.data.metadata.count()
            oj['global_count'] = oj['global_count'] + pj['meta_count']
            pj['meta']=[]
            for meta in proxy.data.metadata.all():
                mj = {}
                mj['id'] = meta.id
                mj['name'] = meta.name
                mj['active'] = meta.active
                pj['meta'].append(mj)
            oj['data'].append(pj)
        
        ret.append(oj)   
        
    proxies = ProxyRequest.objects.filter(owner__isnull=True)
    oj = {}
    
    oj['name']="NOT SET"
    oj['data_count'] = proxies.count()
    oj['global_count'] = 0
    oj['data'] = []
    for proxy in proxies:
        pj = {}
        pj['token']=proxy.token
        pj['url']=proxy.url
        pj['manifest']=proxy.data.manifest
        pj['token']=proxy.token
        
        pj['meta_count']=proxy.data.metadata.count()
        oj['global_count'] = oj['global_count'] + pj['meta_count']
        pj['meta']=[]
        for meta in proxy.data.metadata.all():
            mj = {}
            mj['id'] = meta.id
            mj['name'] = meta.name
            mj['active'] = meta.active
            pj['meta'].append(mj)
        oj['data'].append(pj)
        
    ret.append(oj)   
    return ret  

class Owner(models.Model):
    name = models.CharField(max_length=250)
    group = models.ForeignKey(Group)
    
    def __str__(self):
        return self.name

class ProxyRequest(models.Model):
    owner = models.ForeignKey(Owner, related_name="proxies", null=True, blank=True)
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
    
    def __str__(self):
        return str(self.request)
    
        
class Metadata(models.Model):
    proxy = models.ForeignKey(Proxy, related_name="metadata")
    BB_north = models.FloatField()
    BB_east = models.FloatField()
    BB_south = models.FloatField()
    BB_west = models.FloatField()
    meta = models.TextField()
   
    name = models.TextField()
    
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.proxy) + ":"+ self.name

class MetadataRefreshTime(models.Model):
    metadata = models.ForeignKey(Proxy)
    crontab = models.TextField(default="0 1 * * SAT")
    
    def __str__(self):
        return str(self.metadata) + self.crontab
        
    
