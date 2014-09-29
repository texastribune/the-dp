# TODO switch from relying on initial_data to factories
from django.utils import unittest

from .test_import_thecb_report import *
from .test_models_base import *
from .test_models_reports import *


class ImportReport(unittest.TestCase):
    def test_name_extractor_regexp(self):
        import re

        from tx_highered.scripts.import_report import NAME_EXTRACTOR

        info_strings = (
            ("ACT test scores 2009-10,", ("ACT test scores", "2009-10")),
            ("SAT test scores 2005-06,", ("SAT test scores", "2005-06")),
            ("Admissions 2009-10,", ("Admissions", "2009-10")),
            ("Enrollment by student level Fall 1991,", ("Enrollment by student level", "1991")),
        )

        for info_string, (rn, yr) in info_strings:
            report_name, year_range = re.match(NAME_EXTRACTOR, info_string).groups()
            self.assertEqual(report_name, rn)
            self.assertEqual(year_range, yr)
