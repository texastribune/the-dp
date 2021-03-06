import unittest

from django.test import TestCase

from tx_highered import models
from tx_highered.factories import (InstitutionFactory, EnrollmentFactory,
    )


class InstitutionTestCase(TestCase):
    def setUp(self):
        self.obj = models.Institution.objects.get(
            slug='the-university-of-texas-at-austin')
        self.private_obj = models.Institution.objects.get(
            slug='trinity-university')

    def test_latest_tuition_returns_latest(self):
        latest = self.obj.pricetrends.latest('year')
        self.assertEqual(latest, self.obj.latest_tuition)

    @unittest.skip('publicenrollment is empty in the fixture')
    def test_enrollment_fte_works(self):
        total = self.obj.publicenrollment.latest('year').total
        self.assertEqual(total, self.obj.number_of_full_time_students)

    def test_sentences_property_returns_SummarySentences_object(self):
        self.assertTrue(isinstance(self.obj.sentences,
                models.SummarySentences))

    @unittest.skip('publicenrollment is empty in the fixture')
    def test_latest_public_enrollment(self):
        enrollment = self.obj.latest_enrollment
        self.assertEqual(enrollment, self.obj.publicenrollment.latest('year'))

    def test_latest_private_enrollment(self):
        enrollment = self.private_obj.latest_enrollment
        self.assertEqual(enrollment, self.private_obj.enrollment.latest('year'))

    def test_admissions_latest(self):
        self.obj.admissions.latest

    def test_sentence_institution_type(self):
        self.assertEqual(self.obj.sentence_institution_type,
                         u'public university')
        self.assertEqual(self.private_obj.sentence_institution_type,
                         u'private university')

    def test_enrollment_buckets_work(self):
        institution = InstitutionFactory()

        # trivial case
        data = institution.enrollment_buckets
        self.assertEqual(data['years'], [])

        # add ipeds data
        EnrollmentFactory(
            institution=institution,
            year=2000,
            fulltime_equivalent=100,
        )

        # bust cache
        institution = models.Institution.objects.get(pk=institution.pk)
        data = institution.enrollment_buckets
        # assert year 2000 data appears
        self.assertEqual(data['years'], [2000])
        self.assertEqual(data['fulltime_equivalent'][2000], 100)
