from django.contrib import admin
from signer.models import Petition, Signature

for cls in [Petition, Signature]:
    admin.site.register(cls)
