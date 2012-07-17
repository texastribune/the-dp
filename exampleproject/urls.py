from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


from django.views.generic import View
class Http500View(View):
    def get(self, *args, **kwargs):
        raise Exception("One expects to simply walk into Mordor?")


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tx_highered.views.home', name='home'),
    url(r'', include('tx_highered.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^500/$', Http500View.as_view()),

    url(r'^admin/', include(admin.site.urls)),
)
