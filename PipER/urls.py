from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from data import views as dviews
from broker import views as bviews
from model_manager import views as mviews

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fstatic/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    
         
    url(r'^request/model$', 'model_manager.views.get_model'),
    url(r'^request/getmodel$', 'model_manager.views.get_model_secondary'),
    url(r'^submit/manifest', 'interface.views.approve_manifest'),
    url(r'^federation/new/helo', 'interface.views.start_token'),
    
    url(r'^$', 'interface.views.index'),
    
    url(r'^broker$', 'broker.views.index'),
    url(r'^broker/getproxies$', 'broker.views.index'),
    url(r'^broker/delete/(?P<proxy_id>\w*)$', 'broker.views.delete'),
    url(r'^broker/owners', 'broker.views.all_owners'),
    url(r'^broker/toggle/(?P<id>\d*)$', 'broker.views.toggle'),
    
    url(r'^broker/pull$', 'broker.views.force_pull_remote'),
    url(r'^broker/get$', 'broker.views.force_get_remote'),
    url(r'^broker/clear$', 'broker.views.clear_db'),
    
    url(r'^models$', 'model_manager.views.index'),
    url(r'^models/getmodels$', 'model_manager.views.get_model_secondary'),
    
    
    url(r'^interface/urls$', 'interface.views.urls'),
    url(r'^interface/search$', 'broker.views.search'),
    url(r'^interface/s$', 'broker.views.do_search'),
    url(r'^interface/proxies$', 'broker.views.show'),
    
    url(r'^sld$', 'sldgenerator.views.get_sld'),
    url(r'^external/(?P<path>.*)$', 'interface.views.proxy')
)
