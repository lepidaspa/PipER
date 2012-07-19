from django.contrib import admin
from django.db import models
ProxyRequest = models.get_model("broker", "ProxyRequest")
Proxy = models.get_model("broker", "Proxy")
Metadata = models.get_model("broker", "Metadata")

class ProxyRequestOptions(admin.ModelAdmin):
    save_on_top = True

class ProxyOptions(admin.ModelAdmin):
    save_on_top = True
    
class MetadataOptions(admin.ModelAdmin):
    save_on_top = True
    
    
admin.site.register(ProxyRequest, ProxyRequestOptions)
admin.site.register(Proxy, ProxyOptions)
admin.site.register(Metadata, MetadataOptions)
