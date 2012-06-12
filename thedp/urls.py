from django.conf.urls.defaults import patterns, url
from django.views.generic.list import ListView

from .models import Institution, System
from .views import RenderModelDetailView


urlpatterns = patterns('',
    url(r'^institution/$', ListView.as_view(
        model=Institution), name="institution_list"),
    url(r'^institution/(?P<slug>[-\w]+)/$', RenderModelDetailView.as_view(
        model=Institution, layout="table"), name="institution_detail"),
    url(r'^system/$', ListView.as_view(
        model=System), name="system_list"),
    url(r'^system/(?P<slug>[-\w]+)/$', RenderModelDetailView.as_view(
        model=System, layout="table"), name="system_detail"),
)
