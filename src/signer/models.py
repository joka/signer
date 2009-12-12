# -*- coding: utf-8 -*-

from random import random

from django.db import models
from django.conf import settings
from django.utils.hashcompat import sha_constructor


# this code based in-part on django-registration / django-email-confirmation

class AlreadyConfirmed(Exception):
    pass

class Petition(models.Model):

    title = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20)

    abstract = models.TextField(blank=True)
    text = models.TextField()

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    # adressat
    datenschutz = models.TextField(blank=True, null=True) # what is the email address used for

    def get_absolute_url(self):
        return 'http://%s/%s/'%(settings.BASE_URL, self.short_name)

    def get_signatures(self):
        return self.all_signatures.filter(verified=True)

    def number_signatures(self):
        return self.get_signatures().count()


class Signature(models.Model):
    """
    A single signature of a single person.

    Code is a verification code which is set as long as this signature has not been verified.
    """

    name = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=100)
    
    # comment = models.TextField(blank=True)

    # school
    # position

    timestamp = models.DateTimeField(editable=False, auto_now=True)

    newsletter = models.BooleanField(blank=True, default=True)

    petition = models.ForeignKey('Petition', editable=False, related_name='all_signatures')
    confirmation_code = models.CharField(editable=False, null=True, unique=True, max_length=32)
    verified = models.BooleanField(editable=False, default=False)
    facebook_id = models.CharField(null=True, blank=True, max_length=32)

    @classmethod
    def create_confirm_code(cls, email_address):
        salt = sha_constructor(str(random())).hexdigest()[:5]
        return sha_constructor(salt + email_address).hexdigest()

    def show_confirmation_url(self):
        return 'http://%s/confirm?code=%s'%(settings.BASE_URL, self.confirmation_code)

    class Meta:
        unique_together = (('email_address', 'petition'))
