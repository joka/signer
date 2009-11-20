# -*- coding: utf-8 -*-

from random import random

from django.db import models
from django.utils.hashcompat import sha_constructor


# this code based in-part on django-registration / django-email-confirmation

class AlreadyConfirmed(Exception):
    pass

class Petition(models.Model):

    title = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20)

    text = models.TextField()
    # adressat
    # faq_datenschutz = models.TextField() # what is the email address used for


class Signature(models.Model):
    """
    A single signature of a single person.

    Code is a verification code which is set as long as this signature has not been verified.
    """

    name = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=100)
    comment = models.TextField(blank=True)

    # school
    # position

    timestamp = models.DateTimeField(editable=False, auto_now=True)

    newsletter = models.BooleanField(blank=True, default=True)

    petition = models.ForeignKey('Petition', editable=False)
    confirmation_code = models.CharField(editable=False, null=True, unique=True, max_length=32)
    verified = models.BooleanField(editable=False, default=False)

    def create_confirm_code(cls):
        salt = sha_constructor(str(random())).hexdigest()[:5]
        return sha_constructor(salt + email_address.email).hexdigest()

    def confirm_email(cls, confirmation_code):
        signature = self.get(confirmation_code=confirmation_code)
        if signature.verifed:
            raise AlreadyConfirmed
        signature.verified = True
        signature.save()
        return signature


    def show_confirmation_link(self):
        raise NotYetImplemented

    class Meta:
        unique_together = (('email_address', 'petition'))
