#! /usr/bin/env python
from django.conf import settings
try:
    from django.utils.timezone import now
except ImportError:
    from datetime.datetime import now

import requests
from lxml.html import document_fromstring, tostring

from tx_highered.models import Institution


USER_AGENT = 'thedp-scraper/0.1alpha'


def get_wiki_title(name):
    endpoint = "http://en.wikipedia.org/w/api.php"
    params = dict(action="opensearch",
        search=name,
        limit=1,
        namespace=0,
        format="json",)
    r = requests.get(endpoint, params=params)
    try:
        _, results = r.json
        title = results[0]
    except IndexError:
        return None
    return title


def get_wiki_abstract(url):
    r = requests.get(url, headers={'User-Agent': USER_AGENT})
    doc = document_fromstring(r.text)
    root = doc
    try:
        toc = root.get_element_by_id('toc')
    except KeyError:
        return None
    abstract = []
    for elem in toc.getparent().iterchildren():
        if elem == toc:
            break
        if elem.tag == 'p':
            elem.make_links_absolute(url)
            abstract.append(tostring(elem))
    return "\n".join(abstract).strip()


def get_wiki_seal(inst):
    # TODO move into the model? has unfulfilled requirements: lxml and requests
    url = inst.wikipedia_url
    r = requests.get(url, headers={'User-Agent': USER_AGENT})
    doc = document_fromstring(r.text)
    seals = doc.xpath('//a[@class="image"]/img/@src')
    # lxml doesn't support xpath 2.0, so look for the seal in python
    seals = [x for x in seals if x.lower().find('seal') != -1]
    try:
        seal = seals[0]
    except IndexError:
        return None
    src = "http:" + seal
    dst = "%sseals/%s.png" % (settings.MEDIA_ROOT, inst.slug)
    r = requests.get(src, headers={'User-Agent': USER_AGENT})
    # download to settings.MEDIA_ROOT/seals
    with open(dst, "wb") as f:
        f.write(r.content)
    inst.wikipedia_seal = "seals/%s.png" % inst.slug
    inst.save()
    return inst


def get_titles():
    queryset = Institution.objects.filter(institution_type='uni')
    qs = queryset.filter(wikipedia_title__isnull=True)
    for inst in qs:
        title = get_wiki_title(inst.name)
        if title:
            inst.wikipedia_title = title
            inst.save()
            print inst.name + " -> " + title


def get_abstracts():
    qs = queryset.filter(wikipedia_title__isnull=False, wikipedia_scraped=None)
    for inst in qs:
        text = get_wiki_abstract(inst.wikipedia_url)
        if text:
            inst.wikipedia_abstract = text
            inst.wikipedia_scraped = now()
            inst.save()
            print inst


def get_seals():
    qs = queryset.filter(wikipedia_title__isnull=False, wikipedia_seal="")
    for inst in qs:
        print get_wiki_seal(inst)


if __name__ == "__main__":
    queryset = Institution.objects.filter(institution_type='uni')
