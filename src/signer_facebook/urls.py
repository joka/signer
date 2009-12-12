from django.conf.urls.defaults import *

#Note: views.py depends on these url mappings!

urlpatterns = patterns( 'signer_facebook.views',
    # Petition invite friends form
    (r'^canvas/viewpetition/(?P<petition_name>[-\w]+)/invite/$', 'invitepetition'),
    # Sign petition
    (r'^canvas/viewpetition/(?P<petition_name>[-\w]+)/sign/$', 'signpetition'),
    # List petition signatures
    (r'^canvas/viewpetition/(?P<petition_name>[-\w]+)/signatures/$', 'signatures'),
    # View petition
    (r'^canvas/viewpetition/(?P<petition_name>[-\w]+)/$', 'viewpetition'),
    # Default facebook application callback  page, i.e. what will be seen
    # when you visit http://apps.facebook.com/<appname>.
    (r'^canvas/', 'canvas'),
)
