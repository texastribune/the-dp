from django.conf.urls.defaults import patterns
from django.contrib import admin

from .models import Institution, System


from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin


class DjObjectTools(object):
    change_form_template = "djobjecttools/institution_admin_change_form.html"

    def get_tool_urls(self):
        tools = {}
        for tool in self.djtools:
            tools[tool] = getattr(self, tool)
        my_urls = patterns('',
            (r'^(?P<pk>\d+)/tools/(?P<tool>\w+)/$', self.admin_site.admin_view(
                ModelToolsView.as_view(model=self.model, tools=tools)))
        )
        return my_urls

    def get_urls(self):
        urls = super(DjObjectTools, self).get_urls()
        return self.get_tool_urls() + urls

    def render_change_form(self, request, context, **kwargs):
        context['djtools'] = [(x,
            getattr(getattr(self, x), 'short_description', ''))
            for x in self.djtools]
        return super(DjObjectTools, self).render_change_form(request,
            context, **kwargs)


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


class InstitutionAdmin(DjObjectTools, admin.ModelAdmin):
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

    djtools = ['geocode']

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(System, admin.ModelAdmin)
