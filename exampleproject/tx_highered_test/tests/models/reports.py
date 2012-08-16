from django.test import TestCase
from tx_highered import models


class PriceTrendsTestCase(TestCase):
    def setUp(self):
        self.ut = models.Institution.objects.get(name__endswith='at Austin')
        self.latest = self.ut.latest_tuition

    def test_a_decade_ago_returns(self):
        a_decade_ago = self.latest.a_decade_ago
        self.assertTrue(a_decade_ago.year, self.latest.year - 10)

    def test_in_state_has_risen_true(self):
        self.assertTrue(self.latest.in_state_has_risen)

    def test_in_state_has_risen_false(self):
        old = self.latest.a_decade_ago
        old.tuition_fees_in_state = self.latest.in_state + 1
        self.assertFalse(self.latest.in_state_has_risen)
