from django.test import TestCase
from tx_highered import models


class PriceTrendsTestCase(TestCase):
    def setUp(self):
        # TODO Replace with Factory Boy
        self.ut = models.Institution.objects.get(name__endswith='at Austin')
        self.price_trends = self.ut.latest_tuition

    def test_in_state_maps_to_field(self):
        self.assertEqual(self.price_trends.in_state,
                self.price_trends.tuition_fees_in_state)

    def test_out_of_state_maps_to_field(self):
        self.assertEqual(self.price_trends.out_of_state,
                self.price_trends.tuition_fees_outof_state)

    def test_a_decade_ago_returns(self):
        a_decade_ago = self.price_trends.a_decade_ago
        self.assertTrue(a_decade_ago.year, self.price_trends.year - 10)

    def test_in_state_has_risen_true(self):
        self.assertTrue(self.price_trends.in_state_has_risen)

    def test_in_state_has_risen_false(self):
        old = self.price_trends.a_decade_ago
        old.tuition_fees_in_state = self.price_trends.in_state + 1
        self.assertFalse(self.price_trends.in_state_has_risen)

    def test_out_of_state_has_risen_true(self):
        self.assertTrue(self.price_trends.out_of_state_has_risen)

    def test_out_of_state_has_risen_false(self):
        old = self.price_trends.a_decade_ago
        old.tuition_fees_outof_state = self.price_trends.out_of_state + 1
        self.assertFalse(self.price_trends.out_of_state_has_risen)

    def test_in_state_change(self):
        old = self.price_trends.a_decade_ago
        old.tuition_fees_in_state = self.price_trends.in_state * 0.5
        self.assertEqual(100, self.price_trends.in_state_change)

        old.tuition_fees_in_state = self.price_trends.in_state * 0.25
        self.assertEqual(300, self.price_trends.in_state_change)

        old.tuition_fees_in_state = self.price_trends.in_state * 1.1
        self.assertEqual(10, self.price_trends.in_state_change)

    def test_out_of_state_change(self):
        old = self.price_trends.a_decade_ago
        old.tuition_fees_outof_state = self.price_trends.out_of_state * 0.5
        self.assertEqual(100, self.price_trends.out_of_state_change)

        old.tuition_fees_outof_state = self.price_trends.out_of_state * 0.25
        self.assertEqual(300, self.price_trends.out_of_state_change)

        old.tuition_fees_outof_state = self.price_trends.out_of_state * 1.1
        self.assertEqual(10, self.price_trends.out_of_state_change)


class AdmissionsManagerTestCase(TestCase):
    def setUp(self):
        # TODO Replace with Factory Boy
        self.institute = models.Institution.objects.get(
                name__endswith='at Austin')

    def test_latest_returns_most_recent(self):
        latest = (models.Admissions.objects
                .filter(institution=self.institute).latest('year'))
        self.assertEqual(latest, self.institute.admissions.latest())

    def test_oldest_returns_oldest_model(self):
        oldest = (models.Admissions.objects
                .filter(institution=self.institute).order_by('year')[0])
        self.assertEqual(oldest, self.institute.admissions.oldest())


class AdmissionsTestCase(TestCase):
    def setUp(self):
        # TODO Replace with Factory Boy
        self.institute = models.Institution.objects.get(
                name__endswith='at Austin')
