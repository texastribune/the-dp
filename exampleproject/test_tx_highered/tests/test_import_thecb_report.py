from django.test import TestCase

from tx_highered.scripts.import_thecb_report import parse_header_cell


class Testparse_header_cell(TestCase):
    def test_it_works(self):
        # institution cells
        self.assertEqual(parse_header_cell('Institution'), 'Institution')
        self.assertEqual(parse_header_cell('FICE'), 'FICE')
        self.assertEqual(parse_header_cell('System'), 'System')
        # data cell
        cell = parse_header_cell(
            'First-Time Students in Top 10% (Percent) (Fall 2000)')
        self.assertEqual(cell.long_name,
            'First-Time Students in Top 10% (Percent)')
        self.assertEqual(cell.year, 2000)
        self.assertEqual(cell.year_type, 'fall')
