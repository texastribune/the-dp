from django.test import TestCase
from tx_highered import models


class InstitutionTestCase(TestCase):
    def setUp(self):
        self.obj = models.Institution.objects.get(name__endswith='at Austin')

    def test_latest_tuition_returns_latest(self):
        latest = self.obj.pricetrends.latest('year')
        self.assertEqual(latest, self.obj.latest_tuition)

    def test_number_of_full_time_students(self):
        full_time = self.obj.enrollment.latest('year').fulltime
        self.assertEqual(full_time, self.obj.number_of_full_time_students)

    def test_sentences_property_returns_SummarySentences_object(self):
        self.assertTrue(isinstance(self.obj.sentences,
                models.SummarySentences))

    def test_latest_enrollment(self):
        enrollment = self.obj.latest_enrollment
        self.assertEqual(enrollment, self.obj.enrollment.latest('year'))

    def test_admissions_latest(self):
        self.obj.admissions.latest
