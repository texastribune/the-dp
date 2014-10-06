import os

from django.core.management.base import BaseCommand

from tx_highered.scripts.import_customreport import generic


class Command(BaseCommand):
    args = '(ipeds|thecb) <file file ...>'
    help = "Import Data"

    def handle(self, importer_type, *args, **options):
        # TODO handle THECB data

        if importer_type == 'ipeds':
            for path in args:
                if os.path.isfile(path):
                    generic(path)
