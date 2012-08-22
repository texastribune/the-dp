from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from .models import System
from .views import (HomeView,
                    InstitutionDetailView, InstitutionListView,
                    RenderModelDetailView,
                    TestScoresReport, FunnelReport, Top10RuleReport)


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
    url(r'^testing/$', TestScoresReport.as_view(), name="sat_search"),
    url(r'^funnel/$', FunnelReport.as_view()),
    url(r'^top10/$', Top10RuleReport.as_view()),
) + patterns('tx_highered.api',
    url(r'^api/institution/(?P<pk>\d+)/enrollment/$', 'enrollment_api',
        name='enrollment_api'),
)
