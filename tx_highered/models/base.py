import logging

from django.contrib.gis import geos
from django.contrib.gis.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.template import Context, TemplateDoesNotExist
from django.template.loader import get_template


class SummarySentences(object):
    def __init__(self, obj):
        self.obj = obj
        self.path = '%s/sentences/%s/%%s.txt' % (obj._meta.app_label,
                obj._meta.module_name)
        self.cache = {}

    def __getattr__(self, key):
        if not key in self.cache:
            self.cache[key] = self.generate_sentence(key)
        return self.cache[key]

    def generate_sentence(self, name):
        try:
            t = get_template(self.path % name)
            c = Context({'obj': self.obj})
            return t.render(c).strip()
        except TemplateDoesNotExist:
            return None


APP_LABEL = 'tx_highered'


INSTITUTION_CHOICES = (
        ("uni", "University"),
        ("med", "Health-Related Institutions"),
        ("pub_cc", "Community College"),
        ("pub_tech", "Technical College System"),
        ("pub_state", "State Colleges"),
        ("pri_jr", "Junior College"),
        ("pri_chi", "Chiropractic"),
    )


from geopy import geocoders
from urllib2 import URLError


class ContactFieldsMixin(models.Model):
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    location = models.PointField(geography=True, null=True, blank=True)

    objects = models.GeoManager()

    class Meta:
        abstract = True
        app_label = APP_LABEL

    def _guess_location(self, address_array):
        g = geocoders.Google()
        address = ", ".join(address_array)
        _, latlng = g.geocode(address)
        self.location = geos.fromstr("POINT({0} {1})".format(*latlng))
        self.save()
        return self.location

    def guess_location(self):
        logger = logging.getLogger('tx_highered.models.geolocate')

        # TODO better logging messages
        try:
            guess1 = [self.address, self.city, self.zip_code]
            self._guess_location(guess1)
            logger.debug(self.location)
        except (ValueError, URLError, geocoders.google.GQueryError) as e:
            logger.error("%s %s" % (e.message, ", ".join(guess1)))
            # try again
            try:
                guess2 = [self.name, self.zip_code]
                self._guess_location(guess2)
                logger.debug(self.location)
            except (ValueError, URLError, geocoders.google.GQueryError) as e:
                logger.error("%s %s" % (e.message, ", ".join(guess2)))
        except geocoders.google.GTooManyQueriesError as e:
            logger.error("%s %s" % (e.message, ", ".join(guess1)))


class System(ContactFieldsMixin):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('tx_highered:system_detail', (), {'slug': self.slug})


class WikipediaFields(models.Model):
    # wikipedia
    wikipedia_title = models.CharField(max_length=100, null=True, blank=True)
    wikipedia_abstract = models.TextField(null=True, blank=True)
    wikipedia_seal = models.ImageField(upload_to="seals", null=True, blank=True)
    wikipedia_logo = models.ImageField(upload_to="logos", null=True, blank=True)
    wikipedia_scraped = models.DateTimeField(null=True, blank=True)

    @property
    def wikipedia_url(self):
        if not self.wikipedia_title:
            return None
        return "http://en.wikipedia.org/w/index.php?title=%s" % (
            self.wikipedia_title.replace(" ", "_"))

    class Meta:
        abstract = True


class Institution(ContactFieldsMixin, WikipediaFields):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True)
    is_private = models.BooleanField(default=False)
    institution_type = models.CharField(max_length=30,
            choices=INSTITUTION_CHOICES, null=True, blank=True)
    # administrator officer
    system = models.ForeignKey(System, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # Integrated Postsecondary Education Data System ID
    ipeds_id = models.IntegerField(null=True, blank=True)
    # Federal Interagency Committee on Education ID, used on the State Level
    fice_id = models.IntegerField(null=True, blank=True)
    # Office of Postsecondary Education ID
    # only Title IV schools have this. This is a 6 digit zero padded number with
    # a two digit suffix for each location/branch
    ope_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        if self.system:
            return u"%s - %s" % (self.system, self.name)
        else:
            return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('tx_highered:institution_detail', (), {'slug': self.slug})

    @property
    def type(self):
        return dict(INSTITUTION_CHOICES).get(self.institution_type)

    @property
    def sentences(self):
        if not hasattr(self, '_sentences'):
            self._sentences = SummarySentences(self)
        return self._sentences

    @staticmethod
    def get_unique_name(name):
        ignored = ('st', 'saint', 'college', 'university', 'county', 'district', 'the', 'of', 'at')
        filtered_bits = [x for x in slugify(name).split('-') if x not in ignored]
        return ''.join(filtered_bits)

    @property
    def unique_name(self):
        return Institution.get_unique_name(self.name)

    @property
    def number_of_full_time_students(self):
        enrollment = self.latest_enrollment
        return enrollment.total if enrollment else None

    @property
    def latest_tuition(self):
        return self.pricetrends.latest('year')

    @property
    def latest_enrollment(self):
        try:
            if self.publicenrollment.exists():
                return self.publicenrollment.latest('year')
            else:
                return self.enrollment.latest('year')
        except ObjectDoesNotExist:
            return None


    @property
    def tuition_buckets(self):
        if not hasattr(self, "_tuition_buckets"):
            b = {
                "years": [],
                "in_state": {},
                "out_of_state": {},
                "books_and_supplies": {},
                "room_and_board": {},
            }
            for t in self.pricetrends.all():
                b["years"].append(t.year)
                b["in_state"][t.year] = t.in_state
                b["out_of_state"][t.year] = t.out_of_state
                b["books_and_supplies"][t.year] = t.books_and_supplies
                b["room_and_board"][t.year] = t.room_and_board_on_campus
            self._tuition_buckets = b
        return self._tuition_buckets

    @property
    def sat_score_buckets(self):
        if not hasattr(self, '_sat_score_buckets'):
            b = {
                'years': [],
                'verbal_range': {},
                'math_range': {},
                'writing_range': {},
            }
            for a in self.testscores.all():
                b['years'].append(a.year)
                b['verbal_range'][a.year] = (a.sat_verbal_range
                        if a.sat_verbal_25th_percentile else 'N/A')
                b['math_range'][a.year] = (a.sat_math_range
                        if a.sat_math_25th_percentile else 'N/A')
                b['writing_range'][a.year] = (a.sat_writing_range
                        if a.sat_writing_25th_percentile else 'N/A')
            self._sat_score_buckets = b
        return self._sat_score_buckets

    @property
    def admission_buckets(self):
        if not hasattr(self, '_admission_buckets'):
            b = {
                'years': [],
                'applicants': {},
                'admitted': {},
                'enrolled': {},
            }
            for a in self.admissions.all():
                if not a.number_admitted:
                    continue
                b['years'].append(a.year)
                b['applicants'][a.year] = a.number_of_applicants
                b['admitted'][a.year] = (a.number_admitted,
                        a.percent_of_applicants_admitted)
                b['enrolled'][a.year] = (a.number_admitted_who_enrolled,
                        a.percent_of_admitted_who_enrolled)
            self._admission_buckets = b
        return self._admission_buckets
