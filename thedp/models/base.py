from django.db import models
from django.template.defaultfilters import slugify


__all__ = ['System', 'Institution']


INSTITUTION_CHOICES = (
        ("pub_u", "Public University"),
        ("pub_cc", "Community College"),
        ("pub_med", "Public Health-Related Institutions"),
        ("pub_tech", "Technical College System"),
        ("pub_state", "State Colleges"),
        ("pri_u", "Private University"),
        ("pri_jr", "Junior College"),
        ("pri_med", "Private Health-Related Institutions"),
        ("pri_chi", "Chiropractic"),
    )


class ContactFieldsMixin(models.Model):
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'thedp'


class System(ContactFieldsMixin):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('system_detail', (), {'slug': self.slug})


class Institution(ContactFieldsMixin):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True)
    institution_type = models.CharField(max_length=30,
            choices=INSTITUTION_CHOICES, null=True, blank=True)
    # administrator officer
    system = models.ForeignKey(System, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    # Integrated Postsecondary Education Data System ID
    ipeds_id = models.IntegerField(null=True, blank=True)
    # Office of Postsecondary Education ID
    # only Title IV schools have this. This is a 6 digit zero padded number with
    # a two digit suffix for each location/branch
    ope_id = models.CharField(max_length=8, null=True, blank=True)

    def __unicode__(self):
        if self.system:
            return u"%s - %s" % (self.system, self.name)
        else:
            return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('institution_detail', (), {'slug': self.slug})

    @property
    def type(self):
        return dict(INSTITUTION_CHOICES).get(self.institution_type)

    @staticmethod
    def get_unique_name(name):
        ignored = ('st', 'saint', 'college', 'university', 'county', 'district', 'the', 'of', 'at')
        filtered_bits = [x for x in slugify(name).split('-') if x not in ignored]
        return ''.join(filtered_bits)

    @property
    def unique_name(self):
        return Institution.get_unique_name(self.name)