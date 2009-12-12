# -*- coding: utf-8 -*-

from random import random

from django.db import models
from django.conf import settings 


class Petition_Name(models.Model):
    """
    todo: Wie kann auf die signer.models.Petition Tabelle zugreifen?
    """
    def __unicode__(self):
                return self.petition_name
    petition_name = models.CharField(max_length=100, primary_key=True)

class Signature_Facebook(models.Model):
    """
    A signature representing a facebook user.
    """
    def __unicode__(self):
                return self.facebook_id
    #facebook id user
    facebook_id = models.CharField(max_length=100, primary_key=True)
    #signed petitions
    petitions = models.ManyToManyField('Petition_Name')
    #friends invited to sign
    #todo: make this work
    friends_invited = models.ManyToManyField('Signature_Facebook') 
    #signed friends  
    friends_signed = models.ManyToManyField('Signature_Facebook') 


