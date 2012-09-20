from difflib import get_close_matches

from tx_highered.models import Institution


class FuzzyMatcher(object):
    def __init__(self, qs, field):
        self.lookups = {}
        for o in qs:
            raw_key = getattr(o, field)
            key = self.clean_key(raw_key)
            if key in self.lookups:
                raise ValueError(u"Duplicate key '%s'" % key)
            self.lookups[key] = o

    def clean_key(self, key):
        return key

    def match(self, key):
        key = self.clean_key(key)

        # Return the exact match if it exists
        if key in self.lookups:
            return self.lookups[key]
        # Fall back to the closest matching key
        fuzzy_matches = get_close_matches(key, self.lookups.keys())
        closest_key = fuzzy_matches[0]
        return self.lookups[closest_key]


class InstitutionFuzzyMatcher(FuzzyMatcher):
    def __init__(self):
        qs = Institution.objects.only('id', 'name')
        super(InstitutionFuzzyMatcher, self).__init__(qs, 'name')

    def clean_key(self, key):
        return key.lower()


def create_or_update(objects, **kwargs):
    defaults = kwargs.pop('defaults', {})
    row_count = objects.filter(**kwargs).update(**defaults)
    if row_count:
        return (None, row_count)
    else:
        kwargs.update(defaults)
        obj = objects.create(**kwargs)
        return (obj, 1)
