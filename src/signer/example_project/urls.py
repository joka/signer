from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    )

# singer pyfacebook example
from signer_facebook.urls import urlpatterns as signer_facebook_urlpatterns
urlpatterns += signer_facebook_urlpatterns

# signer example
from signer.urls import urlpatterns as signer_urlpatterns
urlpatterns += signer_urlpatterns


