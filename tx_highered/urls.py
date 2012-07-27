from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, TemplateView

from .models import System
from .views import (InstitutionDetailView, InstitutionListView,
                    RenderModelDetailView, SATListView)


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="tx_highered/index.html"), name="home"),
    url(r'^institution/$', InstitutionListView.as_view(), name="institution_list"),
    url(r'^institution/(?P<slug>[-\w]+)/$', InstitutionDetailView.as_view(),
        name="institution_detail"),
    url(r'^system/$', ListView.as_view(
        model=System), name="system_list"),
    url(r'^system/(?P<slug>[-\w]+)/$', RenderModelDetailView.as_view(
        model=System, layout="table"), name="system_detail"),
    url(r'^testing/$', SATListView.as_view(), name="sat_search"),
)
