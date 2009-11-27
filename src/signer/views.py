# -*- coding: utf-8 -*-

from django import forms
from django.forms.formsets import formset_factory
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.mail import send_mail
from signer.models import Petition, Signature, AlreadyConfirmed


class SignatureForm(forms.ModelForm):

    class Meta:
        model = Signature


EMAIL_TYPES = dict(
    NOT_YET_SIGNED = 0,
    ALREADY_SIGNED = 1,
    ALREADY_SIGNED_AND_CONFIRMED = 2,
    )


def show_petition_list(request):
    return render_to_response('petitionlist.html', {
        'petitions': Petition.objects.all(),
        }, context_instance=RequestContext(request))



def show(request, petition_name):
    petition = get_object_or_404(Petition, short_name=petition_name)
    return render_to_response('show.html', {
        'petition': petition,
        }, context_instance=RequestContext(request))



def sign(request, petition_name):
    petition = get_object_or_404(Petition, short_name=petition_name)

    if request.method == 'POST':

        # validate
        form = SignatureForm(request.POST)

        if form.is_valid():
            email_address = form.cleaned_data['email_address']

            try:
                signature = Signature.objects.get(petition=petition, email_address=email_address)
                if signature.verified:
                    # this is the case if a user has already participated and confirmed

                    email_type = EMAIL_TYPES['ALREADY_SIGNED_AND_CONFIRMED']

                else:
                    # this is the case if a user has already participated but not yet confirmed

                    email_type = EMAIL_TYPES['ALREADY_SIGNED']

            except Signature.DoesNotExist:
                # this is the default case: user signs the petition for the first time

                # generate confirmation code
                confirmation_code = Signature.create_confirm_code(email_address)
                signature = Signature(confirmation_code=confirmation_code, petition=petition)

                email_type = EMAIL_TYPES['NOT_YET_SIGNED']
            
                # send email: again
                # send email: first time

            context = {
                'signature': signature,
                'email_type': email_type,
                'EMAIL_TYPES': EMAIL_TYPES,
                }


            form = SignatureForm(request.POST, instance=signature)
            form.save()

            subject = render_to_string('email_confirmation_subject.txt', context)
            subject = "".join(subject.splitlines())
            message = render_to_string('email_confirmation_message.txt', context)

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                    [email_address])

            return render_to_response('confirm.html', {
                'signature': signature,
                }, context_instance=RequestContext(request))

    else:
        form = SignatureForm()

    return render_to_response('sign.html', {
        'petition': petition,
        'form': form,
        }, context_instance=RequestContext(request))


def confirm(request):

    confirmation_code = request.GET['code']
    signature = get_object_or_404(Signature, confirmation_code=confirmation_code)

    if signature.verified:
        return render_to_response('already_confirmed.html', {
            'signature': signature,
            }, context_instance=RequestContext(request))
    else:
        signature.verified = True
        signature.save()
        return render_to_response('thanks.html', {
            'signature': signature,
            }, context_instance=RequestContext(request))


def list(request, petition_name):
    petition = get_object_or_404(Petition, short_name=petition_name)
    return render_to_response('list.html', {
        'petition': petition
        }, context_instance=RequestContext(request))


class RecommendSenderForm(forms.Form):
    name = forms.CharField(max_length=100)
    email_address = forms.EmailField()

class EmailForm(forms.Form):
    email_address = forms.EmailField()


RecommendReceiverFormSet = formset_factory(EmailForm, extra=settings.NR_RECOMMEND_EMAIL_FIELDS)


def recommend(request, petition_name):
    petition = get_object_or_404(Petition, short_name=petition_name)

    if request.method == 'POST':

        recommend_sender_form = RecommendSenderForm(request.POST, prefix='sender')
        recommend_receiver_formset = RecommendReceiverFormSet(request.POST, prefix='receiver')

        if recommend_sender_form.is_valid() and recommend_receiver_formset.is_valid():

            #import ipdb; ipdb.set_trace()

            for form_dict in recommend_receiver_formset.cleaned_data:
                
                if form_dict=={}: continue

                # TODO: sinnvolles subject, message
                send_mail('Weiterempfehlung der Petition %s'%petition.title, 
                    '%s fordert dich auf, auch an der Petition %s teilzunehmen:\n\n%s'%(recommend_sender_form.cleaned_data['name'], petition.title, petition.get_absolute_url()),
                    settings.DEFAULT_FROM_EMAIL,
                    [form_dict['email_address']])

            return render_to_response('recommend_thanks.html', {
                'recommend_receivers': [],
                }, context_instance=RequestContext(request))

    else:
        recommend_sender_form = RecommendSenderForm(prefix='sender')
        recommend_receiver_formset = RecommendReceiverFormSet(prefix='receiver')

    return render_to_response('recommend.html', {
        'petition': petition,
        'recommend_sender_form': recommend_sender_form,
        'recommend_receiver_formset': recommend_receiver_formset,
        }, context_instance=RequestContext(request))
