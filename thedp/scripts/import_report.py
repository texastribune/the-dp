import sys
import os

from htmltableDictReader import DictReader
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

from thedp.models import Institution


def process_year_based(path):
    report_name = os.path.splitext(os.path.basename(path))[0]
    report_model = report_name.lower()

    Report = ContentType.objects.get(model=report_model).model_class()
    valid_report_fields = Report._meta.get_all_field_names()  # TODO remove fields like `id` ?

    reader = DictReader(open(path, 'r'))
    reader.fieldnames[0] = 'id'
    reader.fieldnames[2] = 'label'
    years_idx_start = 3  # index where field names turn into years

    for row in reader:
        inst = Institution.objects.get(ipeds_id=row['id'])
        report_field = slugify(row['label']).replace('-', '_')
        if report_field in valid_report_fields:
            for year in reader.fieldnames[years_idx_start:]:
                value = row[year]
                if value:
                    r, _ = Report.objects.get_or_create(institution=inst, year=year)
                    setattr(r, report_field, row[year])
                    r.save()


def main():
    path = sys.argv[1]
    process_year_based(path)


if __name__ == "__main__":
    main()
