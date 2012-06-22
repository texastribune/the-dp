import logging  # TODO
import re
import sys
import os

from django.contrib.contenttypes.models import ContentType
from django.db.models import FieldDoesNotExist
from django.template.defaultfilters import slugify

from thedp.models import Institution


class NotImplementedReport(Exception):
    pass


def underscore(s):
    return slugify(s).replace('-', '_')


def get_report(report_model):
    INTERNAL_FIELDS = ['id', 'institution', 'year', 'gender']
    try:
        Report = ContentType.objects.get(model=report_model).model_class()
        valid_report_fields = Report._meta.get_all_field_names()
        valid_report_fields = [x for x in valid_report_fields if x not in INTERNAL_FIELDS]
        unique_together_fields = Report._meta.unique_together[0]
    except ContentType.DoesNotExist:
        raise NotImplementedReport(report_model)
    return Report, unique_together_fields, valid_report_fields


def process_html(path):
    from htmltableDictReader import DictReader

    report_name = os.path.splitext(os.path.basename(path))[0]
    model_model = report_name.replace(" ", "")
    reader = DictReader(open(path, 'r'))
    reader.fieldnames[0] = 'UnitId'
    reader.fieldnames[2] = 'label'
    process_year_based(reader, model_model)

NAME_EXTRACTOR = r"^(.+?)\s(?:Fall\s)?([\-\d]+),$"


def process_csv(path):
    from csv import DictReader

    f = open(path, 'r')
    f.readline()  # skip first line
    info_string = f.readline()
    try:
        report_name, year_range = re.match(NAME_EXTRACTOR, info_string).groups()
        year = year_range[:2] + year_range[-2:]
        model_model = report_name.replace(" ", "")
        reader = DictReader(f)
        process_single_year(year, reader, model_model)
    except AttributeError:
        report_name = re.match(r"(.*) for selected years", info_string).groups()[0]
        model_model = re.sub(r"\W", "", report_name)
        reader = DictReader(f)
        process_year_based(reader, model_model)


def process_year_based(reader, model_model):
    report_model = model_model.lower()

    try:
        Report, unique_together_fields, valid_report_fields = get_report(report_model)
    except NotImplementedReport:
        print "* SAMPLE MODEL CLASS DEF *"
        print "class %s(YearBasedInstitutionStatModel):" % model_model
        for field in reader.fieldnames[2:]:
            if field and not re.match(r"\d+", field):
                print "    %s = models.IntegerField(null=True, blank=True)" % underscore(field)
        raise

    years_idx_start = None
    for i, field in enumerate(reader.fieldnames):
        try:
            int(field)
            years_idx_start = i
            break
        except ValueError:
            pass

    reader.fieldnames = map(underscore, reader.fieldnames)
    unique_together_fields = list(unique_together_fields)
    unique_together_fields.remove('year')  # manually added
    unique_together_fields.remove('institution')  # manually added

    for row in reader:
        if 'label' in reader.fieldnames:
            report_field = underscore(row['label'])
        else:
            report_field = 'value'
            assert 'value' in valid_report_fields

        inst = Institution.objects.get(ipeds_id=row['unitid'])
        get_args = dict(
            institution=inst)
        for field in unique_together_fields:
            get_args[field] = row[field]
        # logger.info(extra_info=row)
        if report_field in valid_report_fields:
            for year in reader.fieldnames[years_idx_start:]:
                value = row[year]
                if value:
                    r, _ = Report.objects.get_or_create(year=year, **get_args)
                    setattr(r, report_field, row[year])
                    r.save()


def process_single_year(year, reader, model_model):
    report_model = model_model.lower()

    try:
        Report, unique_together_fields, valid_report_fields = get_report(report_model)
    except NotImplementedReport:
        print "* SAMPLE MODEL CLASS DEF *"
        print "class %s(YearBasedInstitutionStatModel):" % model_model
        for field in reader.fieldnames[2:]:
            if field:
                print "    %s = models.IntegerField(null=True, blank=True)" % underscore(field)
        raise

    for row in reader:
        inst = Institution.objects.get(ipeds_id=row['UnitId'])
        get_args = dict(institution=inst, year=year)
        data = dict()
        for key, value in row.items():
            value = value.strip()
            if not value:
                continue
            fieldname = underscore(key)

            # translate value
            try:
                model_field = Report._meta.get_field(fieldname)
                if model_field.choices:
                    _ = dict([v, k] for k, v in model_field.choices)
                    value = _[value]  # let this explode with IndexError
            except FieldDoesNotExist:
                # fieldname won't be in unique_together_fields or valid_report_fields
                continue

            if fieldname in unique_together_fields:
                get_args[str(fieldname)] = value
            elif fieldname in valid_report_fields:
                if fieldname.startswith("percent") or fieldname.endswith("percent"):
                    value = value[:-1]  # XXX
                if value:
                    data[fieldname] = value
        r, _ = Report.objects.get_or_create(**get_args)
        r.__dict__.update(data)
        try:
            r.save()
        except ValueError:
            # XXX hack for trying to save bad data
            pass
    print "UPDATED %s %s" % (model_model, year)


def process_file(path):
    print "start process", path
    try:
        report_name, ext = os.path.splitext(os.path.basename(path))
        if ext == ".html":
            process_html(path)
        elif ext == ".csv":
            process_csv(path)
    except NotImplementedReport:
        # logger.error()
        pass
    print "processed", path


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
