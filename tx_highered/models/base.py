import logging
from collections import defaultdict

from django.contrib.gis import geos
from django.contrib.gis.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.template import Context, TemplateDoesNotExist
from django.template.loader import get_template


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


class SentenceDistrict(object):
    def __init__(self, district):
        self.district = district
        self.representative = district.representative

    def __unicode__(self):
        if hasattr(self.district, 'get_absolute_url'):
            district_string = u'<a href="%s">%s</a>' % (
                self.district.get_absolute_url(), self.district)
        else:
            district_string = unicode(self.district)

        if not self.representative:
            return district_string
        elif hasattr(self.representative, 'get_absolute_url'):
            representative_string = u'<a href="%s">%s</a>' % (
                self.representative.get_absolute_url(), self.representative)
        else:
            representative_string = unicode(self.representative)

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
        self.location = geos.fromstr("POINT({1} {0})".format(*latlng))
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

    @models.permalink
    def get_absolute_url(self):
        return ('tx_highered:institution_detail', (), {'slug': self.slug})

    #################### THECB / IPEDS ROUTERS #################
    def get_admissions(self):
        """
        Public universities admissions data comes from the THECB.
        All others use data from IPEDS.
        """
        if not self.is_private and self.institution_type == 'uni':
            return self.publicadmissions
        else:
            return self.admissions

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
    def sentence_districts(self):
        districts = self.lege_districts
        if districts:
            return [SentenceDistrict(d) for d in districts]
        else:
            return None

    ############################## BUCKETS ##############################
    @property
    def tuition_buckets(self):
        fields = ("in_state", "out_of_state", "books_and_supplies", "room_and_board_on_campus")
        return self.get_buckets('pricetrends', fields=fields)

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
            for a in self.get_admissions().all():
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

    @property
    def admission_top10_buckets(self):
        return self.get_buckets('admissions', fields=['percent_top10rule'],
                                 filter_on_field='percent_top10rule')

    def get_buckets(self, relation_name, pivot_on_field="year",
                    filter_on_field=None, fields=None):
        """ pivot a related report model about the year field """
        cache_key = "_%s%s" % (relation_name, len(fields) if fields else "")
        if not hasattr(self, cache_key):
            b = defaultdict(dict)
            b['data_source'] = ""
            pivot_axis = []
            relation = getattr(self, relation_name)
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
            setattr(self, cache_key, b)
            return b
        return getattr(self, cache_key)

    @property
    def enrollment_buckets(self):
        if self.is_private:  # if not self.has_thecb_data
            fields = ("fulltime_equivalent", "fulltime", "parttime")
            b = self.get_buckets("enrollment", fields=fields)
            b['data_source'] = "IPEDS"
            return b
        fields = ("total",)
        b = self.get_buckets("publicenrollment", fields=fields)
        b['data_source'] = "THECB"
        return b

    @property
    def demographics_buckets(self):
        if self.is_private:  # if not self.has_thecb_data
            # hack to hide empty column
            # FIXME assumes white is > 0
            return self.get_buckets("enrollment", filter_on_field="total_percent_white")
        return self.get_buckets("publicenrollment")

    @property
    def graduationrates_buckets(self):
        if self.is_private:
            return self.get_buckets("graduationrates")
        else:
            return self.get_buckets("publicgraduationrates")
