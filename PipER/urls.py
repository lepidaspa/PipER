from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from data import views as dviews
from broker import views as bviews
from model_manager import views as mviews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FiderWeb.views.home', name='home'),
    # url(r'^FiderWeb/', include('FiderWeb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fstatic/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    
         
    url(r'^request/model$', 'mviews.get_model'),
    url(r'^submit/manifest', 'interface.views.approve_manifest'),
    url(r'^federation/new/helo', 'interface.views.start_token'),
    
    url(r'^$', 'interface.views.index'),
    url(r'^interface/urls$', 'interface.views.urls'),
    url(r'^interface/search', 'interface.views.search'),
    url(r'^interface/s', 'interface.views.do_search'),
    
	url(r'^newui/', 'interface.views.newsearch')

    
)
