from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
from django.views.generic import View


admin.autodiscover()


class Http500View(View):
    def get(self, *args, **kwargs):
        raise Exception("One expects to simply walk into Mordor?")


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /",
        mimetype="text/plain")),
    url(r'^500/$', Http500View.as_view()),

    url(r'', include('tx_highered.urls', namespace='tx_highered')),
)

# serve media
# https://docs.djangoproject.com/en/dev/howto/static-files/#serving-other-directories
# doesn't respect settings.MEDIA_URL
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)
