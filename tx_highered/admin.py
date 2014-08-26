from django.contrib import admin

from django_object_actions import DjangoObjectActions

from .models import Institution, System


class InstitutionAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('name', 'ipeds_id', 'fice_id', 'ope_id')
    list_filter = ('institution_type', 'is_private')
    # list_editable = ('ipeds_id', 'fice_id', 'ope_id')
    ordering = ('name', )

    def geocode(self, request, obj):
        old_location = obj.location
        obj.guess_location()
        if old_location != obj.location:
            obj.save()
            self.message_user(request, "Location Updated To: %s" % obj.location)
        else:
            self.message_user(request, "Location Unchanged")
    geocode.short_description = u"Remember to save before using"

    objectactions = ['geocode']

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(System, admin.ModelAdmin)
