from django.db import models


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
    # administrator officer
    system = models.ForeignKey(System, null=True, blank=True)

    def __unicode__(self):
        if self.system:
            return u"%s - %s" % (self.system, self.name)
        else:
            return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('institution_detail', (), {'slug': self.slug})
