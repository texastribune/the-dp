import logging  # TODO
import re
import sys
import os

from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

from thedp.models import Institution


class NotImplementedReport(Exception):
    pass


def underscore(s):
    return slugify(s).replace('-', '_')


def get_report(report_model):
    try:
        Report = ContentType.objects.get(model=report_model).model_class()
        valid_report_fields = Report._meta.get_all_field_names()  # TODO remove fields like `id` ?
    except ContentType.DoesNotExist:
        raise NotImplementedReport(report_model)
    return Report, valid_report_fields


def process_year_based(path):
    from htmltableDictReader import DictReader

    report_name = os.path.splitext(os.path.basename(path))[0]
    report_model = report_name.lower()

    Report, valid_report_fields = get_report(report_model)

    reader = DictReader(open(path, 'r'))
    reader.fieldnames[0] = 'UnitId'
    reader.fieldnames[2] = 'label'
    years_idx_start = 3  # index where field names turn into years

    for row in reader:
        inst = Institution.objects.get(ipeds_id=row['UnitId'])
        report_field = underscore(row['label'])
        # logger.info(extra_info=row)
        if report_field in valid_report_fields:
            for year in reader.fieldnames[years_idx_start:]:
                value = row[year]
                if value:
                    r, _ = Report.objects.get_or_create(institution=inst, year=year)
                    setattr(r, report_field, row[year])
                    r.save()


def process_single_year(path):
    from csv import DictReader

    f = open(path, 'r')
    f.readline()  # skip first line
    info_string = f.readline()
    report_name, year_range = re.match(r"^(.+)\s([\-\d]+),$", info_string).groups()
    year = year_range[:2] + year_range[-2:]
    report_model = report_name.replace(" ", "").lower()

    Report, valid_report_fields = get_report(report_model)

    reader = DictReader(f)

    for row in reader:
        inst = Institution.objects.get(ipeds_id=row['UnitId'])
        data = dict()
        for key, value in row.items():
            if not value:
                continue
            fieldname = underscore(key)
            if fieldname in valid_report_fields:
                if fieldname.endswith("percent"): value = value[:-1]  # XXX
                data[fieldname] = value
        r, _ = Report.objects.get_or_create(institution=inst, year=year)
        r.__dict__.update(data)
        r.save()


def process_file(path):
    try:
        report_name, ext = os.path.splitext(os.path.basename(path))
        if ext == ".html":
            process_year_based(path)
        elif ext == ".csv":
            process_single_year(path)
    except NotImplementedReport:
        # logger.error()
        pass


def main():
    path = sys.argv[1]

    if os.path.isdir(path):
        files = []
        for foo in os.walk(path):
            files.extend([os.path.join(foo[0], bar) for bar in foo[2]])
        for filepath in files:
            process_file(filepath)
    else:
        process_file(path)


if __name__ == "__main__":
    main()
