# -*- coding: utf-8 -*-

from datetime import datetime
import re
from django.conf import settings
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
    
    def assertEmail(self, recipients=None, from_email=None, subject_snippets=[], body_snippets=[]):
        """ looks up if given subject, body, recipients and sender email match
        with any email in the django outbox. for subject and recipients a list of
        matching substrings has to be given."""

        def checkEmail(email):
            return ((recipients is None) or (email.recipients()==recipients)) \
                    and ((from_email is None) or (email.from_email==from_email)) \
                    and all([snippet in email.subject for snippet in subject_snippets]) \
                    and all([snippet in email.body for snippet in body_snippets])

        matches = filter(checkEmail, mail.outbox)

        if matches == []:
            raise self.failureException("No email matched the following criteria:\n\nrecipients: %r\nfrom_email: %r\nsubject_snippets: %r\nbody_snippets: %r" %
                    (recipients, from_email, subject_snippets, body_snippets))
        else:
            return matches



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

        nr_emails_before = len(mail.outbox)
        response = self.c.post(reverse('signer.views.sign', kwargs={'petition_name': PETITION['short_name']}), {
            'name': u'Larissa Löwenzahn',
            'email_address': u'lara@example.com',
            })
        self.assertContains(response, 'Du hast eine Mail bekommen')
        self.assertEquals(len(mail.outbox), nr_emails_before + 1)
        matches = self.assertEmail(recipients=[u'lara@example.com'], subject_snippets=[u'Bitte bestätige'], body_snippets=[u'Liebe/r Larissa'])
        link = self.get_confirmation_link(matches[-1].body)

        response = self.c.get(link, follow=True)
        self.assertContains(response, u'Larissa Löwenzahn')
        self.assertContains(response, u'Danke für die Teilnahme')
        self.assertContains(response, 'weiterempfehlen')
        
        self.assertEquals(self.pet.number_signatures(), 1)

        response = self.c.get(link, follow=True)
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

    def recommend(self, from_name, from_email, to_emails):
        response = self.c.get(reverse('signer.views.recommend', kwargs={'petition_name': PETITION['short_name']}))
        values = dict([('receiver-%d-email_address'%nr, to_emails[nr] if nr<len(to_emails) else '') for nr in range(settings.NR_RECOMMEND_EMAIL_FIELDS)])
        values.update({
                'sender-name': from_name,
                'sender-email_address': from_email,
                'receiver-TOTAL_FORMS': unicode(settings.NR_RECOMMEND_EMAIL_FIELDS),
                'receiver-INITIAL_FORMS': u'0',
                })
        response = self.c.post(reverse('signer.views.recommend', kwargs={'petition_name': PETITION['short_name']}), values) 
            
        for to_email in to_emails:
            self.assertEmail(recipients = [to_email], body_snippets = [from_name, self.pet.get_absolute_url()])

        self.assertContains(response, 'wurden versendet')
            

    
    def test_recommend(self):
        self.recommend('Nina Hager', 'nina@example.com', ['friend1@example.com', 'friend2@example.com'])


