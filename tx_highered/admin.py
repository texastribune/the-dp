from django.conf.urls.defaults import patterns
from django.contrib import admin

from .models import Institution, System


from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin


class DjObjectTools(object):
    def get_tool_urls(self):
        tools = {}
        for tool in self.djtools:
            tools[tool] = getattr(self, tool)
        my_urls = patterns('',
            (r'^(?P<pk>\d+)/tools/(?P<tool>\w+)/$', self.admin_site.admin_view(
                ModelToolsView.as_view(model=self.model, tools=tools)))
        )
        return my_urls


class ModelToolsView(SingleObjectMixin, View):
    tools = {}

    def get(self, request, **kwargs):
        obj = self.get_object()
        try:
            self.tools[kwargs['tool']](request, obj)
        except KeyError:
            raise Http404
        back = request.path.rsplit('/', 3)[0] + '/'
        return HttpResponseRedirect(back)

    def message_user(self, request, message):
        # copied from django.contrib.admin.options
        messages.info(request, message)


class InstitutionAdmin(admin.ModelAdmin, DjObjectTools):
    list_display = ('name', 'ipeds_id', 'fice_id', 'ope_id')
    list_filter = ('institution_type', 'is_private')
    # list_editable = ('ipeds_id', 'fice_id', 'ope_id')
    ordering = ('name', )

    def get_urls(self):
        # TODO make this magical
        urls = super(InstitutionAdmin, self).get_urls()
        return self.get_tool_urls() + urls

    def geocode(self, request, obj):
        old_location = obj.location
        obj.guess_location()
        if old_location != obj.location:
            obj.save()
            self.message_user(request, "Location Updated To: %s" % obj.location)
        else:
            self.message_user(request, "Location Unchanged")

    djtools = ['geocode']

    class Media:
        js = ("djobjecttools/djobjecttools.js", )


admin.site.register(Institution, InstitutionAdmin)
admin.site.register(System, admin.ModelAdmin)
