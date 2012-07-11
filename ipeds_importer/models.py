from django.db import models


class Variable(models.Model):
    """ An IPEDS report variable """
    code = models.CharField(max_length=20)
    short_name = models.CharField(max_length=8)
    category = models.CharField(max_length=150)
    long_name = models.CharField(max_length=80)
    raw = models.CharField(max_length=800, unique=True)


from django.contrib import admin


class VariableAdmin(admin.ModelAdmin):
    list_display = ('long_name', 'code', 'short_name', 'category')
    list_filter = ('code', 'short_name')
    list_per_page = 250  # limit of 250 variables per report

    def make_MVL(self, request, queryset):
        from django.http import HttpResponse
        from datetime import datetime
        response = HttpResponse("".join(queryset.values_list('raw', flat=True)),
            mimetype="text/plain")
        filename = datetime.now().isoformat().split('.')[0].replace(':', '-')
        filename += "-q%s" % queryset.count()
        response['Content-Disposition'] = 'attachment; filename=ipeds-%s.mvl' % filename
        return response
    actions = ['make_MVL']

admin.site.register(Variable, VariableAdmin)
