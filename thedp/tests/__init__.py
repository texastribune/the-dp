# from django.utils import unittest
import unittest


class ImportReport(unittest.TestCase):
    def testBasic(self):
        a = ['larry', 'curly', 'moe']
        self.assertEqual(a[0], 'larry')
