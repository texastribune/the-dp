from django.contrib import admin
from .models import Institution, System


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'ipeds_id', 'fice_id', 'ope_id')
    list_filter = ('institution_type', 'is_private')
    # list_editable = ('ipeds_id', 'fice_id', 'ope_id')
    ordering = ('name', )

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(System, admin.ModelAdmin)
