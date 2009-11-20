# -*- coding: utf-8 -*-

from django import forms
from django.shortcuts import render_to_response, get_object_or_404
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


def signer(request, petition_name):

    petition = get_object_or_404(Petition, short_name=petition_name)


    if request.method == 'POST':

        # validate
        form = SignatureForm(request.POST)

        if form.is_valid():
            email_address = form.cleaned_data['email_address']

            try:
                signature = Petition.objects.get(petition=petition, email_address=email_address)
                if signature.is_verified():
                    # this is the case if a user has already participated and confirmed

                    email_type = EMAIL_TYPES['ALREADY_SIGNED_AND_CONFIRMED']

                else:
                    # this is the case if a user has already participated but not yet confirmed

                    email_type = EMAIL_TYPES['ALREADY_SIGNED']

            except Signature.DoesNotExist:
                # this is the default case: user signs the petition for the first time

                # generate confirmation code
                confirmation_code = Signature.create_unique_code()
                signature = Signature(confirmation_code=confirmation_code, petition=petition)

                email_type = EMAIL_TYPES['NOT_YET_SIGNED']
            
                # send email: again
                # send email: first time

            context = {
                'signature': signature,
                'repeated': repeated,
                'email_type': email_type,
                'EMAIL_TYPES': EMAIL_TYPES,
                })

            subject = render_to_string('email_confirmation_subject.txt', context)
            subject = "".join(subject.splitlines())
            message = render_to_string('email_confirmation_message.txt', context)

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                    [email_address])


            form = SignatureForm(instance=signature)
            form.save()


            return render_to_response('confirm.html')

        else: # invalid form
            return render_to_response('sign.html', {
                'petition': petition,
                'form': form,
                })

    else:
        form = SignatureForm()

        return render_to_response('sign.html', {
            'petition': petition,
            'form': form,
            })


def confirm(request):

    confirmation_code = request.GET['code']
    try:
        Signature.confirm_email(confirmation_code)

    except AlreadyConfirmed:
        raise NotYetImplemented
    except Signature.DoesNotExist:
        raise NotYetImplemented



def list_signatures(request):
    raise NotYetImplemented
