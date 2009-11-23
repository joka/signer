from django.contrib import admin
from signer.models import Petition, Signature

class PetitionAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'title')

admin.site.register(Petition, PetitionAdmin)

# don't put signature in admin interface because of privacy

#for cls in [Signature]:
    #admin.site.register(cls)

