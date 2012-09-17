#! /usr/bin/env python
#
# The admissions data is loaded from PDF reports on the THECB website.
#
# To preprocess:
#
# find . -name "*.pdf" -exec pdf2json -i {} \;
# find . -name "*[0-9]" -exec sh -c 'jsonpp "$1" > "$1.pdf.json"' -- {} \;
# find . -name "*[0-9]" -delete
#
import HTMLParser
import json
import sys
from pprint import pprint


class Node(object):
    def __init__(self, text):
        self.__dict__.update(text)
        self.left = text['left']
        self.top = text['top']
        self.data = text['data']

    @property
    def begins_institution_name(self):
        return 10 <= self.left <= 15 and 60 <= self.top <= 70

    @property
    def begins_enrollment(self):
        return 15 <= self.left <= 20 and self.data.startswith('Enrollment')

    @property
    def begins_acceptance(self):
        return 15 <= self.left <= 20 and self.data.startswith('Acceptance')

    @property
    def total_value(self):
        # TODO: parse out the total from continuous values
        return self.data


class Parser(object):
    def __init__(self):
        self._cache = []
        self.records = {}
        self._html_parser = HTMLParser.HTMLParser()

        # State
        self._current_institution = None
        self._expect_acceptance = False
        self._expect_enrollment = False

    def _clean_row(self, record):
        # Parse applications
        if (self._cache[0].data.startswith('Total')
                and self._cache[1].data.startswith('Applicants')):
            record['data'].append(('applicants', self._cache[-1].total_value))

        # Parse admissions
        if self._cache[0].begins_acceptance:
            self._expect_acceptance = True
        elif (self._expect_acceptance
                and self._cache[0].data.startswith('Total')
                and self._cache[1].data.startswith('Accepted')):
            record['data'].append(('admissions', self._cache[-1].total_value))
            self._expect_acceptance = False

        # Parse enrollment
        if self._cache[0].begins_enrollment:
            self._expect_enrollment = True
        elif self._expect_enrollment:
            record['data'].append(('enrollment', self._cache[-1].total_value))
            self._expect_enrollment = False

    def flush(self, new_page=False):
        if not self._cache:
            return

        # Parse institution name
        if self._cache[0].begins_institution_name:
            institution = ''.join([n.data for n in self._cache])
            self._current_institution = self._html_parser.unescape(institution)

        # Get or create record for institution
        if self._current_institution:
            if self._current_institution in self.records:
                record = self.records[self._current_institution]
            else:
                record = self.records[self._current_institution] = {
                    'institution': self._current_institution,
                    'data': [],
                }

            # Save any relevant data for this record
            self._clean_row(record)

        self._cache = []

    def feed(self, text):
        node = Node(text)
        if self._cache and node.top - self._cache[-1].top > 20:
            self.flush()
        self._cache.append(node)

    def iter_results(self):
        keys = sorted(self.records.keys())
        for key in keys:
            yield self.records[key]


def main(path):
    json_text = open(path).read().decode('iso-8859-1')
    json_data = json.loads(json_text)
    parser = Parser()
    for page_data in json_data:
        for el in page_data['text']:
            parser.feed(el)
        parser.flush(new_page=True)

    for record in parser.iter_results():
        pprint(record)


if __name__ == '__main__':
    main(sys.argv[1])
