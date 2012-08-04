#! /usr/bin/env python

import requests

from tx_highered.models import Institution

qs = Institution.objects.filter(wikipedia__isnull=True)


def get_wiki_url(name):
    endpoint = "http://en.wikipedia.org/w/api.php"
    params = dict(action="opensearch",
        search=name,
        limit=1,
        namespace=0,
        format="json",)
    r = requests.get(endpoint, params=params)
    try:
        _, results = r.json
        article = results[0].replace(' ', '_')
    except IndexError:
        return None
    return "http://en.wikipedia.org/wiki/%s" % article


if __name__ == "__main__":
    for inst in qs:
        url = get_wiki_url(inst.name)
        if url:
            inst.wikipedia = url
            inst.save()
            print inst, url
