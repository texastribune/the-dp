#! /usr/bin/env python
#
# DEPRECATED in favor of just using the IPEDS data to avoid having to deal with
# scraping PDFs. We can't automate this, and it's costing us too much time to
# wrangle with this data source.
#
# The admissions data is loaded from PDF reports on the THECB website.
#
# Use pdftohtml to preprocess:
#
# find . -name "*.pdf" -exec sh -c 'pdftohtml -i -noframes -stdout "$1" > "$1.html"' -- {} \;
#
import glob
import HTMLParser
import os
import re
import sys
from collections import defaultdict
from decimal import Decimal
from pprint import pprint

from tx_highered.models import PublicAdmissions
from tx_highered.thecb_importer.utils import (InstitutionFuzzyMatcher,
        create_or_update)


class Node(object):
    html_parser = HTMLParser.HTMLParser()

    def __init__(self, line):
        self.data = line.strip().replace('<br>', '')

        self.is_empty = False
        self.is_number = False
        self.is_institution = False
        self.is_page_break = False
        self.is_row_header = False

        unescaped_data = self.html_parser.unescape(self.data)

        # Mark nodes we don't care about as empty
        if not self.data or 'BODY>' in self.data or 'HTML>' in self.data:
            self.is_empty = True

        # HR elements signify page breaks
        elif self.data == '<hr>':
            self.is_page_break = True

        # Sometimes multiple numbers appear in the same textbox.
        # We only need the last one since we only care about totals.
        elif re.match(r'^[\d,]+(\s[\d,]+)*$', self.data):
            self.is_number = True
            last_number = self.data.split()[-1].replace(',', '')
            self.data = int(last_number)

        # Institutions are the only non-numeric uppercase lines
        elif unescaped_data.upper() == unescaped_data:
            self.is_institution = True
            self.data = unescaped_data

        elif self.data in ('Total Texas', 'Top 10%',
                           'Enrolled, other Texas public university'):
            self.is_row_header = True

    def __repr__(self):
        return u'<Node: %r>' % self.data


class Parser(object):
    def __init__(self, path):
        self.path = path
        self.data = defaultdict(dict)

        # Parse year from path name
        name = os.path.basename(path).replace('.pdf.html', '')
        self.year = int(name.split('_')[1])

        # Store parser state
        self.cache = []
        self.in_body = False
        self.institution = None
        self.expected_field = None

    def feed(self, line):
        node = Node(line)
        # print node

        # The body begins after the first page break
        if node.is_page_break:
            self.in_body = True
            self.institution = None
            return

        # Skip everything before the body
        if not self.in_body:
            return

        # Return if the node is empty
        if node.is_empty:
            return

        # Expect data after seeing an institution
        if node.is_institution:
            self.institution = node.data

        # If we reach the end of a row and expect data, the last field
        # of the row contains the value for the expected field.
        if node.is_row_header and self.expected_field and self.cache:
            institution_data = self.data[self.institution]
            institution_data[self.expected_field] = self.cache[-1].data
            self.expected_field = None
            self.cache = []

        # Cache numbers until finding an expected value
        elif node.is_number:
            self.cache.append(node)

        # Set expected field from the row header
        if not self.institution:
            return
        if node.data == 'Total Applicants':
            self.expected_field = 'applied'
        elif node.data == 'Total Accepted':
            self.expected_field = 'accepted'
        elif node.data == 'Total Enrolled':
            self.expected_field = 'enrolled'

    def parse(self):
        for line in open(self.path):
            self.feed(line)


def derive_rate(numerator, denominator):
    if denominator == 0 or numerator > denominator:
        return None
    else:
        return round(100.0 * numerator / denominator, 2)


def main(root):
    for path in glob.glob(os.path.join(root, '*.pdf.html')):
        parser = Parser(path)
        parser.parse()
        matcher = InstitutionFuzzyMatcher()
        for institution, data in parser.data.iteritems():
            attrs = dict(institution=institution, year=parser.year, **data)

            # Derive acceptance and enrollment rates
            acceptance_rate = derive_rate(data['accepted'], data['applied'])
            enrollment_rate = derive_rate(data['enrolled'], data['accepted'])

            # Create or update institution admissions for this year
            institution = matcher.match(institution)
            defaults = {
                'year_type': 'fall',
                'number_of_applicants': data['applied'],
                'number_admitted': data['accepted'],
                'number_admitted_who_enrolled': data['enrolled'],
                'percent_of_applicants_admitted': acceptance_rate,
                'percent_of_admitted_who_enrolled': enrollment_rate
            }
            obj, row_count = create_or_update(PublicAdmissions.objects,
                    institution=institution, year=parser.year,
                    defaults=defaults)
            if obj:
                print 'created %s %d admissions...' % (
                    institution.name, parser.year)
            else:
                print 'updated %s %d admissions...' % (
                    institution.name, parser.year)


if __name__ == '__main__':
    main(sys.argv[1])
