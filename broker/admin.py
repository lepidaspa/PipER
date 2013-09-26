from django.contrib import admin
from django.db import models

from  broker.models import * 

class ProxyRequestOptions(admin.ModelAdmin):
    save_on_top = True
    def has_add_permission(self, request):
        return False

class ProxyOptions(admin.ModelAdmin):
    save_on_top = True
    def has_add_permission(self, request):
        return False
    
class MetadataOptions(admin.ModelAdmin):
    save_on_top = True
    def has_add_permission(self, request):
        return False
    
class MetadataRefreshTimeOptions(admin.ModelAdmin):
    save_on_top = True
    def has_add_permission(self, request):
        return False
    
    
admin.site.register(ProxyRequest, ProxyRequestOptions)
admin.site.register(Proxy, ProxyOptions)
admin.site.register(Metadata, MetadataOptions)
admin.site.register(MetadataRefreshTime, MetadataRefreshTimeOptions)
admin.site.register(Owner)
