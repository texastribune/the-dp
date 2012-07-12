import csv
import re
from collections import defaultdict


class IpedsCsvReader(object):
    field_mapping = None
    primary_mapping = None
    year_type = None

    def __init__(self, fh, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self._reader = self.get_reader(fh)
        self.parse_header()

    def get_reader(self, fh):
        return csv.reader(fh)

    def parse_header(self):
        header = self._reader.next()
        self.header = header
        if self.field_mapping is None:
            return
        years = defaultdict(list)
        fields = dict(self.field_mapping)
        primary_idx = None
        for idx, cell in enumerate(header):
            if cell == self.primary_mapping[0]:
                primary_idx = idx
                continue
            try:
                name, year = re.match(r'(\w+)\([a-zA-Z]+(\d+)', cell).groups()
            except AttributeError:
                continue
            if name in fields:
                years[year].append((idx, fields[name]))
        self.primary_idx = primary_idx
        self.years_data = years

    def parse_rows(self, institution_model, report_model):
        for row in self._reader:
            inst = institution_model.objects.get(ipeds_id=row[self.primary_idx])
            for year in self.years_data:
                instance, _ = report_model.objects.get_or_create(
                    institution=inst, year=year,
                    defaults=dict(year_type=self.year_type))
                for idx, name in self.years_data[year]:
                    if row[idx]:
                        setattr(instance, name, row[idx])
                instance.save()
                print instance

    def explain_header(self):
        from .models import Variable
        name_set = set()
        for cell in self.header:
            try:
                name, code = re.match(r'(\w+)\((\w+)\)', cell).groups()
                var = Variable.objects.filter(raw__startswith="%s|%s|" % (code, name))[0]
            except AttributeError:
                continue
            except IndexError:
                name = "????"
                code = cell
                var = None
            name_set.add(name)
            print name, code, var.long_name if var else ""
        print "%d Unique Variables: %s" % (len(name_set), sorted(name_set))
