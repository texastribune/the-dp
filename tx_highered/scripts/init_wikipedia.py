#! /usr/bin/env python
from django.conf import settings
try:
    from django.utils.timezone import now
except ImportError:
    from datetime.datetime import now

import os
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


def get_wiki_images(inst):
    # TODO move into the model? has unfulfilled requirements: lxml and requests
    url = inst.wikipedia_url
    r = requests.get(url, headers={'User-Agent': USER_AGENT})
    doc = document_fromstring(r.text)
    images = doc.xpath('//table[@class="infobox vcard"]//a[@class="image"]/img/@src')

    # look for a seal
    seals = [x for x in images if x.lower().find('seal') != -1]
    try:
        seal = seals[0]
    except IndexError:
        seal = None
    if seal and not inst.wikipedia_seal:
        src = "http:" + seal
        # download to settings.MEDIA_ROOT/seals, upload_to="seals"
        dst_path = "seals/%s-seal.png" % inst.slug
        dst_abspath = os.path.join(settings.MEDIA_ROOT, dst_path)
        r = requests.get(src, headers={'User-Agent': USER_AGENT})
        with open(dst_abspath, "wb") as f:
            f.write(r.content)
        inst.wikipedia_seal = dst_path
        inst.save()

    # now look for a logo using the exact same code as above for some reason
    logos = [x for x in images if x not in seals]
    try:
        logo = logos[0]
    except IndexError:
        logo = None
    if logo and not inst.wikipedia_logo:
        src = "http:" + logo
        # download to settings.MEDIA_ROOT/logos, upload_to="logos"
        dst_path = "logos/%s-logo.png" % inst.slug
        dst_abspath = os.path.join(settings.MEDIA_ROOT, dst_path)
        r = requests.get(src, headers={'User-Agent': USER_AGENT})
        with open(dst_abspath, "wb") as f:
            f.write(r.content)
        inst.wikipedia_logo = dst_path
        inst.save()

    return inst


def get_titles():
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


def get_images():
    qs = queryset.filter(wikipedia_title__isnull=False)
    for inst in qs:
        print get_wiki_images(inst)


if __name__ == "__main__":
    queryset = Institution.objects.filter(institution_type='uni')
