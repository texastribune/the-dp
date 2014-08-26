from django.conf.urls import patterns, url
from django.views.generic import ListView

from .models import System
from .views import (HomeView,
                    InstitutionDetailView, InstitutionListView,
                    RenderModelDetailView,
                    TestScoresReport, FunnelReport, Top10RuleReport)
from . import api


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^institutions/$', InstitutionListView.as_view(),
        name="institution_list"),
    url(r'^system/$', ListView.as_view(
        model=System), name="system_list"),
    url(r'^system/(?P<slug>[-\w]+)/$', RenderModelDetailView.as_view(
        model=System, layout="table"), name="system_detail"),
    # reports
    url(r'^testing/$', TestScoresReport.as_view(), name="sat_search"),
    url(r'^funnel/$', FunnelReport.as_view()),
    url(r'^top10/$', Top10RuleReport.as_view()),
    url(r'^(?P<slug>[-\w]+)/$', InstitutionDetailView.as_view(),
        name="institution_detail"),
) + patterns('tx_highered.api',
    url(r'^api/institution/(?P<pk>\d+)/enrollment/$', 'enrollment_api',
        name='enrollment_api'),
    url(r'^api/institution/(?P<pk>\d+)/(?P<metric>\w+)/$',
        api.ReportView.as_view(report_name='testscores'),
        name='institution_api'),
    url(r'^api/institution/$', 'institution_api', name='institution_api'),
)
