# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^sign/?P<petition_name>\w+$', 'signer.views.signer'),
    (r'^confirm$', 'signer.views.confirm'),
)
