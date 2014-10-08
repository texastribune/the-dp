import factory

from . import models


class InstitutionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Institution

    name = factory.Sequence(lambda i: u'Institution {}'.format(i))
    slug = factory.Sequence(lambda i: u'institution-{}'.format(i))


class BaseReportFactory(factory.DjangoModelFactory):
    institution = factory.SubFactory(InstitutionFactory)


class EnrollmentFactory(BaseReportFactory):
    FACTORY_FOR = models.Enrollment


class PublicEnrollmentFactory(BaseReportFactory):
    FACTORY_FOR = models.PublicEnrollment
