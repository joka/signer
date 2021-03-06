# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<petition_name>[-\w]+)/$', 'signer.views.show'),
    (r'^(?P<petition_name>[-\w]+)/sign/$', 'signer.views.sign'),
    (r'^(?P<petition_name>[-\w]+)/list/$', 'signer.views.list'),
    (r'^(?P<petition_name>[-\w]+)/recommend/$', 'signer.views.recommend'),
    (r'^confirm$', 'signer.views.confirm'),
    (r'^contact$', 'signer.views.contact'),
    (r'^$', 'signer.views.show_petition_list'),
)
