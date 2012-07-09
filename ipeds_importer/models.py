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
    list_display = ('code', 'short_name', 'category', 'long_name')
    list_filter = ('code', 'short_name')

admin.site.register(Variable, VariableAdmin)
