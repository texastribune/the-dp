#! /usr/bin/env python
import datetime

import requests
from lxml.html import parse, tostring

from tx_highered.models import Institution


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


def get_wiki_abstract(url):
    doc = parse(url)  # won't handle https
    root = doc.getroot()
    toc = root.get_element_by_id('toc')
    abstract = []
    for elem in toc.getparent().iterchildren():
        if elem == toc:
            break
        if elem.tag == 'p':
            elem.make_links_absolute()
            abstract.append(tostring(elem))
    return "\n".join(abstract).strip()


def main():
    queryset = Institution.objects.filter(institution_type='uni')
    qs = queryset.filter(wikipedia__isnull=True)
    for inst in qs:
        url = get_wiki_url(inst.name)
        if url:
            inst.wikipedia = url
            inst.save()
            print inst, url

    qs = queryset.filter(wikipedia__isnull=False)
    for inst in qs:
        text = get_wiki_abstract(inst.wikipedia)
        if text:
            inst.wikipedia_abstract = text
            inst.wikipedia_scaped = datetime.datetime.now()
            inst.save()
            print inst


if __name__ == "__main__":
    main()
