from django.db import models

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

    # hi
    ipeds_id = models.IntegerField(null=True, blank=True)

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
