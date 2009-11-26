# -*- coding: utf-8 -*-

from datetime import datetime
import re
from django.core import mail
from django.core.urlresolvers import reverse
from django.forms.fields import url_re
from django.test import TestCase
from django.test.client import Client
from signer.models import Petition, Signature


PETITION = {
        'title': 'Forderungen der FU Berlin',
        'short_name': 'fu-forderungen',
        'abstract': 'Wir wollen einiges anders',
        'text': u'''* Keine Studiengebühren\n* Mehr Studium Generale''',
        'datenschutz': u'''Die E-Mail-Adresse wird sorgsam behandelt.''',
        'start_date': datetime.now(),
        }


class RichTestCase(TestCase):

    def assertValidUrl(self, value):
        if url_re.search(value) is None:
            raise ValueError, 'URL is not valid: %r'%value

    def assertIn(self, text, snippet):
        if not snippet in text:
            raise AssertionError('--\n%s\n--\nnot in\n--\n%s\n--'%(snippet, text))


class SignerTest(RichTestCase):

    def get_confirmation_link(self, text):
        link = re.compile(r'.*folgenden Link:\n\n([^\n]*)\n.*').search(text).groups()[0]
        #import ipdb; ipdb.set_trace()
        self.assertValidUrl(link)
        return link

    def setUp(self):
        self.pet = Petition.objects.create(**PETITION)
        self.c = Client()

    def show_petition_list(self):
        response = self.c.get(reverse('signer.views.show_petition_list'))
        self.assertContains(response, PETITION['title'])
        self.assertContains(response, PETITION['short_name'])

    def show_pet(self):
        response = self.c.get(reverse('signer.views.show', kwargs={'petition_name': PETITION['short_name']}))
        self.assertContains(response, PETITION['text'])
        self.assertContains(response, PETITION['title'])
        self.assertContains(response, 'Ja - ich unterschreibe')
        self.assertContains(response, str(self.pet.number_signatures()))

    def sign_pet(self):
        response = self.c.get(reverse('signer.views.sign', kwargs={'petition_name': PETITION['short_name']}))
        self.assertContains(response, PETITION['text'])
        self.assertContains(response, PETITION['title'])
        self.assertContains(response, str(self.pet.number_signatures()))

        response = self.c.post(reverse('signer.views.sign', kwargs={'petition_name': PETITION['short_name']}), {
            'name': u'Larissa Löwenzahn',
            'email_address': u'lara@example.com',
            })
        self.assertContains(response, 'Du hast eine Mail bekommen')
        self.assertEquals(len(mail.outbox), 1)
        self.assertIn(mail.outbox[0].subject, u'Bitte bestätige')
        self.assertIn(mail.outbox[0].body, u'Liebe/r Larissa')
        link = self.get_confirmation_link(mail.outbox[0].body)

        response = self.c.get(link)
        self.assertContains(response, u'Hallo Larissa Löwenzahn')
        self.assertContains(response, u'Danke für die Teilnahme')
        
        self.assertEquals(self.pet.number_signatures(), 1)

        response = self.c.get(link)
        self.assertContains(response, u'Hallo Larissa Löwenzahn')
        self.assertContains(response, u'Bestätigungslink wurde bereits zuvor geklickt')

    def show_signatures(self):
        response = self.c.get(reverse('signer.views.list', kwargs={'petition_name': PETITION['short_name']}))
        self.assertContains(response, u'Larissa Löwenzahn')

    def test_default_path(self):
        """
        currently only tests that the default path is okay
        """
        self.assertEquals(self.pet.number_signatures(), 0)
        self.show_petition_list()
        self.show_pet()
        self.sign_pet()
        self.show_signatures()

