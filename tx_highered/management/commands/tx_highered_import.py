import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import Data"

    def handle(self, *args, **options):
        # TODO handle THECB data
        from tx_highered.scripts.import_customreport import generic

        for path in args:
            if os.path.isfile(path):
                generic(path)
