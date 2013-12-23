from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from ecloud_web.views import *

import os.path
site_media = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'site_media')

def i18n_javascript(request):
    return admin.site.i18n_javascript(request)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ecloud.views.home', name='home'),
    # url(r'^ecloud/', include('ecloud.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/jsi18n', i18n_javascript),
    url(r'^admin/', include(admin.site.urls)),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', main_page),
    
    # session management
    url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^login/$', login_page),
    url(r'^logout/$', logout_page),
    url(r'^register/$', register_page),
    url(r'^register/success/$', TemplateView.as_view(template_name='registration/register_success.html')),
    
    # order
    url(r'^user/view_order/$', view_order_page),
    url(r'^user/order_instance/$', order_instance_page),
    url(r'^order/(.*)/update/$', order_update_page),
    url(r'^order/list/$', order_list_page),

    # Instance
    url(r'^instance/(.*)/console/$', instance_vnc_console_page),
    url(r'^instance/action/$', instance_action_page),
    url(r'^instance/list/$', instance_list_page),

    # order
    url(r'^resource/usage/$', resource_usage_page),
    
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media} )
)
