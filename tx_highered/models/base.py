import logging
from collections import defaultdict
from urllib2 import URLError

from django.contrib.gis import geos
from django.contrib.gis.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template import Context, TemplateDoesNotExist
from django.template.defaultfilters import slugify
from django.template.loader import get_template
from django.utils.functional import cached_property

try:
    from geopy import geocoders
    CAN_GEOCODE = True
except ImportError:
    CAN_GEOCODE = False

from tx_lege_districts.models import District
from tx_lege_districts.constants import SBOE


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


class DistrictsSentence(object):
    def __init__(self, obj, *districts):
        self.obj = obj
        self.districts = districts

    def __unicode__(self):
        clauses = map(self.make_clause, self.districts)
        if len(clauses) <= 2:
            joined_clauses = u' and '.join(clauses)
        else:
            clauses[-1] = u'and %s' % (clauses[-1])
            joined_clauses = ', '.join(clauses)

        return u'%s is represented by %s' % (
            self.obj.sentence_name, joined_clauses)

    def make_clause(self, district):
        representative = district.representative
        if hasattr(district, 'get_absolute_url'):
            district_string = u'<a href="%s">%s</a>' % (
                district.get_absolute_url(), district)
        else:
            district_string = unicode(district)

        if not representative:
            return district_string
        elif hasattr(representative, 'get_absolute_url'):
            representative_string = u'<a href="%s">%s</a>' % (
                representative.get_absolute_url(), representative)
        else:
            representative_string = unicode(representative)

        return u'%s in %s' % (representative_string, district_string)


APP_LABEL = 'tx_highered'


INSTITUTION_CHOICES = (
        ("uni", "University"),
        ("med", "Health-Related Institutions"),
        ("pub_cc", "Community College"),
        ("pub_tech", "Technical College System"),
        ("pub_state", "State Colleges"),
        ("pri_jr", "Junior College"),
        ("pri_chi", "Chiropractic Institution"),
    )


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
        if not CAN_GEOCODE:
            return
        g = geocoders.Google()
        address = ", ".join(address_array)
        _, latlng = g.geocode(address)
        self.location = geos.fromstr("POINT({1} {0})".format(*latlng))
        self.save()
        return self.location

    def guess_location(self):
        logger = logging.getLogger('tx_highered.models.geolocate')
        if not CAN_GEOCODE:
            logger.error(u'Attempted to geocode without geopy installed')
            return

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

    def get_absolute_url(self):
        return reverse('tx_highered:system_detail', kwargs={'slug': self.slug})


class WikipediaFields(models.Model):
    # wikipedia
    wikipedia_title = models.CharField(max_length=100, null=True, blank=True)
    wikipedia_abstract = models.TextField(null=True, blank=True)
    wikipedia_seal = models.ImageField(upload_to="%s/seals" % APP_LABEL,
        null=True, blank=True)
    wikipedia_logo = models.ImageField(upload_to="%s/logos" % APP_LABEL,
        null=True, blank=True)
    wikipedia_scraped = models.DateTimeField(null=True, blank=True)

    @property
    def wikipedia_url(self):
        if not self.wikipedia_title:
            return None
        return "http://en.wikipedia.org/w/index.php?title=%s" % (
            self.wikipedia_title.replace(" ", "_"))

    class Meta:
        abstract = True


class InstitutionManager(models.GeoManager):
    def published(self):
        """ only return institutions ready to be shown """
        qs = self.get_query_set()
        return qs.filter(Q(ipeds_id__isnull=False) | Q(fice_id__isnull=False)).\
            exclude(Q(institution_type='med') | Q(institution_type='pri_chi'))


class Institution(ContactFieldsMixin, WikipediaFields):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True)
    is_private = models.BooleanField(default=False)
    institution_type = models.CharField(max_length=30,
            choices=INSTITUTION_CHOICES, null=True, blank=True)
    # administrator officer
    system = models.ForeignKey(System, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # WISHLIST change these institution identifiers to be charfields instead of
    # ints so we can do zero-padding because that's how they're reported,
    # except then it'll be harder to look up institutions because you'll have
    # to be careful about '0's.

    # Integrated Postsecondary Education Data System ID
    ipeds_id = models.IntegerField(null=True, blank=True)
    # Federal Interagency Committee on Education ID, used on the State Level
    fice_id = models.IntegerField(null=True, blank=True)
    # Office of Postsecondary Education ID
    # only Title IV schools have this. This is a 6 digit zero padded number with
    # a two digit suffix for each location/branch
    ope_id = models.IntegerField(null=True, blank=True)

    objects = InstitutionManager()

    def __unicode__(self):
        if self.system:
            return u"%s - %s" % (self.system, self.name)
        else:
            return self.name

    def get_absolute_url(self):
        return reverse(
            'tx_highered:institution_detail', kwargs={'slug': self.slug})

    #################### THECB / IPEDS ROUTERS #################
    def get_admissions(self):
        """
        Get admissions data. First, try IPEDS, then, try THECB.
        """
        # if not self.is_private and self.institution_type == 'uni':
        #     return self.publicadmissions.all()
        return self.admissions.all()

    def get_graduation_rates(self):
        """
        Public institutions use THECB graduation rates; others use IPEDS.
        """
        if not self.is_private:
            return self.publicgraduationrates.all()
        else:
            return self.graduationrates.all()

    @property
    def type(self):
        """ Get human readable version of `institution_type` """
        return dict(INSTITUTION_CHOICES).get(self.institution_type)

    @property
    def sentences(self):
        """ Get a generated sentence about the `Institution` """
        # TODO use cache backend (was caching in memory)
        return SummarySentences(self)

    # DELETEME replace with fuzzy matcher or can just delete
    @staticmethod
    def get_unique_name(name):
        ignored = ('st', 'saint', 'college', 'university', 'county', 'district', 'the', 'of', 'at')
        filtered_bits = [x for x in slugify(name).split('-') if x not in ignored]
        return ''.join(filtered_bits)

    # DELETEME replace with fuzzy matcher or can just delete
    @property
    def unique_name(self):
        return Institution.get_unique_name(self.name)

    @property
    def logo(self):
        """ return the `Image` that represents the logo or `None` """
        return self.wikipedia_logo

    @property
    def seal(self):
        """ return the `Image` that represents the seal or `None` """
        return self.wikipedia_seal

    @cached_property
    def enrollment_fte(self):
        """
        Quick stat to find out how many students are enrolled.

        Designed to answer the question, "so how many students are at ____?"
        Uses full time equivalent so community colleges with lots of part-time
        enrollment aren't inflated.
        """
        enrollment = self.enrollment.latest('year')
        return enrollment.fulltime_equivalent if enrollment else None

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
    def sentence_name(self):
        if self.name.startswith('University'):
            return u'The %s' % self.name
        else:
            return self.name

    @property
    def sentence_institution_type(self):
        institution_type = self.get_institution_type_display().lower()
        if self.is_private:
            return u'private %s' % institution_type
        else:
            return u'public %s' % institution_type

    @property
    def geojson(self):
        from tx_highered.api import JSON
        if self.location:
            return JSON(self.location.geojson)
        else:
            return None

    @property
    def lege_districts(self):
        location = self.location
        if not location:
            return None

        return (District.objects.filter(geometry__contains=location.wkt)
                .exclude(type=SBOE))

    @property
    def districts_sentence(self):
        districts = self.lege_districts
        if districts:
            return DistrictsSentence(self, *districts)
        else:
            return None

    ############################## BUCKETS ##############################
    @cached_property
    def tuition_buckets(self):
        fields = ("in_state", "out_of_state", "books_and_supplies", "room_and_board_on_campus")
        return self.get_buckets('pricetrends', fields=fields)

    @cached_property
    def sat_score_buckets(self):
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
        return b

    @cached_property
    def admission_buckets(self):
        b = {
            'years': [],
            'applicants': {},
            'admitted': {},
            'enrolled': {},
        }
        for a in self.get_admissions().all():
            if not a.number_admitted:
                continue
            b['years'].append(a.year)
            b['applicants'][a.year] = a.number_of_applicants
            b['admitted'][a.year] = (a.number_admitted,
                    a.percent_of_applicants_admitted)
            b['enrolled'][a.year] = (a.number_admitted_who_enrolled,
                    a.percent_of_admitted_who_enrolled)
        return b

    @cached_property
    def admission_top10_buckets(self):
        return self.get_buckets('admissions', fields=['percent_top10rule'],
                                filter_on_field='percent_top10rule')

    def get_buckets(self, relation_name, pivot_on_field="year",
                    filter_on_field=None, fields=None):
        """ pivot a related report model about the year field """
        b = defaultdict(dict)
        pivot_axis = []
        relation = getattr(self, relation_name)
        b['data_source'] = relation.model.data_source
        if fields is None:
            # XXX requires instacharts
            fields = [x[0] for x in relation.model.get_chart_series() if x[0] != pivot_on_field]
        for report_obj in relation.all():
            if filter_on_field is not None:
                # make sure we want this data
                filter_value = getattr(report_obj, filter_on_field)
                if filter_value is None or filter_value is '':
                    # null or blank
                    continue
            pivot = getattr(report_obj, pivot_on_field)
            pivot_axis.append(pivot)
            for field in fields:
                b[field][pivot] = getattr(report_obj, field)
        b[pivot_on_field + "s"] = pivot_axis  # poor man's `pluralize()`
        return b

    @cached_property
    def enrollment_buckets(self):
        """Get enrollment data from IPEDS."""
        b = self.get_buckets("enrollment",
            fields=("fulltime_equivalent", "fulltime", "parttime"))
        b['data_source'] = "IPEDS"
        return b

    @cached_property
    def demographics_buckets(self):
        """
        Get the most recent demographics data.

        Sometimes ipeds has better data, sometimes it's thecb. There isn't a
        magic way to figure out which is the latest without manually checking.

        XXX assumes school has white people.
        """
        try:
            latest_ipeds = self.enrollment.filter(
                total_percent_white__isnull=False).latest('year').year
        except ObjectDoesNotExist:
            latest_ipeds = 0
        try:
            latest_thecb = self.publicenrollment.filter(
                white_percent__isnull=False).latest('year').year
        except ObjectDoesNotExist:
            latest_thecb = 0
        if latest_ipeds > latest_thecb:
            return self.get_buckets("enrollment", filter_on_field="total_percent_white")
        return self.get_buckets("publicenrollment")

    @cached_property
    def graduationrates_buckets(self):
        if self.is_private:
            return self.get_buckets("graduationrates")
        else:
            return self.get_buckets("publicgraduationrates")
