#! /usr/bin/env python
import datetime

import requests
from lxml.html import parse, tostring

from tx_highered.models import Institution


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
    qs = queryset.filter(wikipedia_title__isnull=True)
    for inst in qs:
        title = get_wiki_title(inst.name)
        if title:
            inst.wikipedia_title = title
            inst.save()
            print inst.name + " -> " + title

    qs = queryset.filter(wikipedia_title__isnull=False, wikipedia_scraped=None)
    for inst in qs:
        text = get_wiki_abstract(inst.wikipedia_url)
        if text:
            inst.wikipedia_abstract = text
            inst.wikipedia_scraped = datetime.datetime.now()
            inst.save()
            print inst


if __name__ == "__main__":
    main()
