from django.contrib import admin
from django.db import models

from  broker.models import * 

class ProxyRequestOptions(admin.ModelAdmin):
    save_on_top = True

class ProxyOptions(admin.ModelAdmin):
    save_on_top = True
    
class MetadataOptions(admin.ModelAdmin):
    save_on_top = True
    
class MetadataRefreshTimeOptions(admin.ModelAdmin):
    save_on_top = True
    
    
admin.site.register(ProxyRequest, ProxyRequestOptions)
admin.site.register(Proxy, ProxyOptions)
admin.site.register(Metadata, MetadataOptions)
admin.site.register(MetadataRefreshTime, MetadataRefreshTimeOptions)
