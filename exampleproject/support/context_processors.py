from django.conf import settings


def bootstrap_context(request):
    ctx = {}

    ctx.update({
        "SITE_NAME": settings.SITE_NAME,
        # "SITE_DOMAIN": site.domain
    })

    return ctx
