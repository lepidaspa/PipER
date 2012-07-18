from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from interface import views as iviews
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
    
         
    url(r'^request/model$', mviews.get_model),
    url(r'^submit/manifest', iviews.approve_manifest),
    url(r'^federation/new/helo', iviews.start_token),
    
    url(r'^$', iviews.index),
    url(r'^interface/search', bviews.search),
    url(r'^interface/s', bviews.do_search),

    
)
