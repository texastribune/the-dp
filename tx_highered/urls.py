from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from .models import System
from .views import (HomeView,
                    InstitutionDetailView, InstitutionListView,
                    RenderModelDetailView, SATListView, FunnelListView)


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^institution/$', InstitutionListView.as_view(), name="institution_list"),
    url(r'^institution/(?P<slug>[-\w]+)/$', InstitutionDetailView.as_view(),
        name="institution_detail"),
    url(r'^system/$', ListView.as_view(
        model=System), name="system_list"),
    url(r'^system/(?P<slug>[-\w]+)/$', RenderModelDetailView.as_view(
        model=System, layout="table"), name="system_detail"),
    # reports
    url(r'^testing/$', SATListView.as_view(), name="sat_search"),
    url(r'^funnel/$', FunnelListView.as_view()),
)
