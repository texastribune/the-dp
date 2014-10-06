import os

from django.core.management.base import BaseCommand, CommandError

from tx_highered.scripts.import_customreport import generic as ipeds
from tx_highered.scripts.import_thecb_report import generic as thecb


class Command(BaseCommand):
    args = '(ipeds|thecb) <file file ...>'
    help = "Import Data"

    def handle(self, importer_type, *args, **options):
        # WISHLIST handle verbosity option

        if importer_type == 'ipeds':
            for path in args:
                if os.path.isfile(path):
                    ipeds(path)
        elif importer_type == 'thecb':
            for path in args:
                if os.path.isfile(path):
                    thecb(path)
        else:
            raise CommandError(u'Not a valid importer type: "{}"'
                .format(importer_type))
