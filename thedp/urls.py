from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView, TemplateView

from .models import Institution, System
from .views import InstitutionListView, RenderModelDetailView, SATListView, DegreesListView


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="thedp/index.html"), name="home"),
    url(r'^institution/$', InstitutionListView.as_view(), name="institution_list"),
    url(r'^institution/(?P<slug>[-\w]+)/$', DetailView.as_view(
        model=Institution), name="institution_detail"),
    url(r'^system/$', ListView.as_view(
        model=System), name="system_list"),
    url(r'^system/(?P<slug>[-\w]+)/$', RenderModelDetailView.as_view(
        model=System, layout="table"), name="system_detail"),
    url(r'^SAT/$', SATListView.as_view(), name="sat_search"),
    url(r'^degrees/$', DegreesListView.as_view(), name="degrees_count"),
)
