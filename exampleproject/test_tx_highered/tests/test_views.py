from django.test import TestCase, RequestFactory

from tx_highered.factories import InstitutionFactory, EnrollmentFactory
from tx_highered.views import HomeView, LATEST_ENROLLMENT_YEAR


class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_trivial_works(self):
        request = self.factory.get('/foo/')
        view = HomeView.as_view()
        # trivial case with no content
        with self.assertNumQueries(0):
            response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_get_short_list_trivial_works(self):
        # setup
        view = HomeView()

        with self.assertNumQueries(1):
            short_list = list(view.get_short_list())
        self.assertFalse(short_list)

    def test_get_short_list_returns_enrollments(self):
        # setup
        view = HomeView()
        institution = InstitutionFactory()
        EnrollmentFactory(institution=institution, year=LATEST_ENROLLMENT_YEAR)

        with self.assertNumQueries(1):
            short_list = list(view.get_short_list())
        self.assertEqual(short_list[0].institution, institution)
