import logging

from django.contrib.gis import geos
from django.contrib.gis.db import models
# from django.db import models
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
        return self.latest_enrollment.total

    @property
    def latest_tuition(self):
        return self.pricetrends.latest('year')

    @property
    def latest_enrollment(self):
        if self.is_private:
            return self.enrollment.latest('year')
        else:
            return self.publicenrollment.latest('year')
