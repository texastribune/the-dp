#! /usr/bin/env python
#
# DEPRECATED This logic is too difficult to maintain. Use the accountability
# search data for graduation rates instead.
#
# Almanac graduation rates are on page 21 of the 2012 THECB Almanac.
# We are only interested in the 2011 rates; the others are loaded from
# the accountability reports.
#
# To preprocess:
#
# $ brew install pdf2json jsonpp
# $ pdf2json -f 21 -l 21 THECB2012almanacweb20120516.pdf
# $ jsonpp THECB2012almanacweb20120516 > almanac_p21.pdf.json
#
from __future__ import absolute_import

import HTMLParser
import json
import re
import sys

from tx_highered.models import Institution, PublicGraduationRates
from tx_highered.thecb_importer.utils import (InstitutionFuzzyMatcher,
        create_or_update)

NAME_RE = re.compile(r"^([^\d\/\%]+)")


class Node(object):
    def __init__(self, text):
        self.__dict__.update(text)
        self.left = text['left']
        self.top = text['top']
        self.data = text['data']

    @property
    def in_bounds(self):
        return self.left < 580 and 300 < self.top < 1420


class Parser(object):
    def __init__(self):
        self._cache = []
        self._rows = []
        self._html_parser = HTMLParser.HTMLParser()

    def _clean_row(self, row):
        # Join all data in the row
        text = ' '.join([node.data for node in row])
        # Preprocess 'n/a' values so all values can be split along '%'
        text = text.replace(' n /a  ', '%n/a%')
        # Extract the institution name so only values remain
        match = NAME_RE.match(text)
        assert match
        name = match.group(0)
        values = text.replace(name, '')
        # Clean name and parse any HTML entities
        cleaned_name = re.sub('\s+', ' ', name).strip('* ')
        cleaned_name = self._html_parser.unescape(cleaned_name)
        # Clean values
        cleaned_values = [v.strip() for v in values.split('%') if v.strip()]
        cleaned_values = [v if v != 'n/a' else None for v in cleaned_values]
        # Expect 13 values: 2000 through 2011 and percent change
        assert len(cleaned_values) == 13
        # The 2011 value is the second to last
        return cleaned_name, cleaned_values[-2]

    def flush(self):
        if self._cache:
            self._rows.append(self._cache)
            self._cache = []

    def feed(self, text):
        node = Node(text)
        if node.in_bounds:
            self._cache.append(node)
        else:
            self.flush()

    def iter_results(self):
        self.flush()
        for row in self._rows:
            yield self._clean_row(row)


def main(path):
    # Parse 2011 6-year graduation rates
    json_text = open(path).read().decode('iso-8859-1')
    page_data = json.loads(json_text)[0]
    parser = Parser()
    for el in page_data['text']:
        parser.feed(el)

    # Match institutions by name and create or update
    matcher = InstitutionFuzzyMatcher()
    for name, bachelor_6yr in parser.iter_results():
        institution = matcher.match(name)
        defaults = dict(bachelor_6yr=bachelor_6yr)
        obj, row_count = create_or_update(PublicGraduationRates.objects,
                institution=institution, year=2011, defaults=defaults)
        if obj:
            print "created %s graduation rates..." % institution.name
        else:
            print "updated %s graduation rates..." % institution.name


if __name__ == '__main__':
    main(sys.argv[1])
