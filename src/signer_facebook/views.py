# -*- coding: utf-8 -*-

from urllib import urlencode
from cgi import escape 

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.http import urlencode
from django.http import HttpResponse, HttpResponseRedirect

from django.utils.decorators import decorator_from_middleware
from facebook.djangofb import FacebookMiddleware
import facebook.djangofb as facebook 

from signer.models import Petition 
from signer_facebook.models import Petition_Name, Signature_Facebook
import signer_facebook.decorators as signer_facebook


#cached outsourced methods 

#def get_petition_title(petition_short_name):
    
#    petition = get_object_or_404(Petition, short_name=petition_name)


#def get_petition_absolute_url(petition_short_name):

#    petition = get_object_or_404(Petition, short_name=petition_name)


#view methods:

@decorator_from_middleware(FacebookMiddleware)
@facebook.require_login()
def canvas(request):

    fb_uid = request.facebook.uid
    sf = Signature_Facebook(facebook_id = fb_uid)

    vars = {}
    vars['petitions'] = Petition.objects.all()
    vars['mypetitions'] = sf.petitions.all() 
    vars['fb_url'] = request.facebook.get_app_url()  
    
    return render_to_response('canvas.fbml', vars, context_instance=RequestContext(request))


@decorator_from_middleware(FacebookMiddleware)
@signer_facebook.require_add(next= lambda request: '/'.join(request.path.split('/')[2:]))
def viewpetition(request, petition_name):

    petition = get_object_or_404(Petition, short_name=petition_name)
    fb = request.facebook
    sf = Signature_Facebook(facebook_id = fb.uid)

    vars = {}
    vars['signed'] = petition_name in map(str, sf.petitions.all()) 
    vars['iframe_url'] = petition.get_absolute_url() + '?&show_actions='
    vars['fb_url'] = fb.get_app_url()   
    vars['fb_url_pet'] = "%sviewpetition/%s/"  % (vars['fb_url'], petition_name)   
    
    return render_to_response('show.fbml', vars)


@decorator_from_middleware(FacebookMiddleware)
@signer_facebook.require_add(next= lambda request: '/'.join(request.path.split('/')[2:]))
def signpetition(request, petition_name):

    petition = get_object_or_404(Petition, short_name=petition_name)
    fb = request.facebook
    sf = Signature_Facebook(facebook_id = fb.uid)
    #todo:facebook errors?
    name = escape(fb.users.getInfo([fb.uid], ['name'])[0][u'name'])
    url_params = urlencode({'name': name, 'facebook_id': fb.uid})

    vars = {}
    vars['petition_title'] = petition.title
    vars['signed'] = petition_name in map(str, sf.petitions.all()) 
    vars['iframe_url'] ="%ssign/?%s" % (petition.get_absolute_url(), url_params) 
    vars['fb_url'] = fb.get_app_url()   
    vars['fb_url_pet'] = "%sviewpetition/%s/"  % (vars['fb_url'], petition_name)  
    
    return render_to_response('sign.fbml', vars)
 

@decorator_from_middleware(FacebookMiddleware)
@signer_facebook.require_add(next= lambda request: '/'.join(request.path.split('/')[2:]))
def invitepetition(request, petition_name):
    
    petition = get_object_or_404(Petition, short_name=petition_name)
    fb = request.facebook
    sf = Signature_Facebook(facebook_id = request.facebook.uid)
 
    vars = {}
    vars['signed'] = petition_name in map(str, sf.petitions.all()) 
    vars['fb_url'] = fb.get_app_url()   
    vars['fb_url_pet'] = "%sviewpetition/%s/"  % (vars['fb_url'], petition_name)   
    vars['petition_title'] = petition.title
    
    # exclude already signed friends
    pet = Petition_Name(petition_name=petition_name)
    signatures = [str(x.facebook_id) for x in pet.signature_facebook_set.all()]
    friends = request.facebook.friends.get()
    friends_signed = filter(lambda x: x in signatures, friends) 
    vars['exclude_ids'] = ",".join(map(str, friends_signed)) 
    #invitation message
    vars['app_name'] = fb.app_name
    content = \
       u""" <fb:name uid="%s" firstnameonly="true" shownetwork="True"/> \
              möchte dich einladen die Bildungsstreikpetition \
              %s \
              zu unterstützen, \
            <fb:req-choice url="%s" label="Petition unterstützen"/>  \
        """ % (fb.uid, vars['petition_title'], vars['fb_url_pet'])
    vars['content'] = escape(content, True) 
   
    return render_to_response('invite.fbml', vars) 


@decorator_from_middleware(FacebookMiddleware)
@signer_facebook.require_add(next= lambda request: '/'.join(request.path.split('/')[2:]))
def signatures(request, petition_name):
    
    petition = get_object_or_404(Petition, short_name=petition_name)
    fb = request.facebook
    sf = Signature_Facebook(facebook_id = request.facebook.uid)
 
    vars = {}
    vars['signed'] = petition_name in map(str, sf.petitions.all()) 
    vars['iframe_url'] = petition.get_absolute_url() + 'list/' 
    vars['fb_url'] = fb.get_app_url()   
    vars['fb_url_pet'] = "%sviewpetition/%s/"  % (vars['fb_url'], petition_name)   

    return render_to_response('show.fbml', vars) 
