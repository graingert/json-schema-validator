"""
URL mappings for the Dashboard application

Those mappings are only effective during testing
"""
from django.conf.urls.defaults import *
from django.contrib import databrowse
from django.views.generic.simple import direct_to_template

from dashboard_app import urls
from dashboard_app.views import auth_test
from dashboard_app.views import dashboard_xml_rpc_handler

# Start with empty pattern list 
urlpatterns = patterns('')
# Append original urls (we don't want to alter them)
urlpatterns += urls.urlpatterns
# Append our custom extra urls
urlpatterns += patterns('',
    url(r'^auth-test/', auth_test))

# Append default URLs from dashboard_server so that our templates do not
# blow up trying to reverse URL them.
urlpatterns += patterns('',
    url(r'^$', direct_to_template,
        name='home',
        kwargs={'template': 'index.html'}),
    url(r'^about/$', direct_to_template,
        name='about',
        kwargs={'template': 'about.html'}),
    url(r'^data/(.*)', databrowse.site.root,
        name='data-browser'),
    url(r'xml-rpc/', dashboard_xml_rpc_handler,
        name='xml-rpc'))
