from django.contrib import admin
from .models import Institution, System


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'ipeds_id', 'fice_id', 'ope_id')
    list_filter = ('institution_type',)
    list_editable = ('ipeds_id', 'fice_id', 'ope_id')

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(System, admin.ModelAdmin)
