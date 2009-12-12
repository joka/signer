"""
Signer-Facebook app
====================


This django app is a facebook application, so you need FACEBOOK_API_KEY, 
FACEBOOK_SECRET_KEY and FACEBOOK_APP_NAME in you settings. On the Facebook applications page, 
make sure that you set your callback to the appropriate URL. 
('http://YOUR_IP/canvas/')  and Render Method (FBML). 

It only works together with the signer app. The facebook startpage (canvas) lists available
petitions and the petitions the facebook user has signed.
The petition views are are mainly iframes to the runnung singer app
(have a look at urls.py, views.py).

The django model Signer_Facebook represents a facebook user,
>>> from signer_facebook.models import Signature_Facebook, Petition_Name
>>> s1= Signature_Facebook(facebook_id="234")
>>> s1.save()
>>> s1
<Signature_Facebook: 234>

Petition_Name a petition:
>>> p1=Petition_Name(petition_name="test1")
>>> p1.save()
>>> p1            
<Petition_Name: test1>


When a facebook user goes to sign a petition, a note is send to his wall and
the petition name is saved:
>>> s1.petitions.add(p1)
>>> s1.save()
>>> s1.petitions.all()
[<Petition_Name: test1>]

This way  we  can  also see, who has signed de petition:
>>> p1.signature_facebook_set.all()
[<Signature_Facebook: 234>]

#We can also invite other users and see if they join in:
#>>> s2= Signature_Facebook(facebook_id="2345")
#>>> s2.save()
#>>> s1.friends_invited.add(s2)
#>>> s1.friends_invited.all()  
#[<Signature_Facebook: 2345>]

"""
