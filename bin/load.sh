cd $(cat $VIRTUAL_ENV/.project)/tx_highered/scripts

DJANGO_SETTINGS_MODULE=exampleproject.settings

# These locations are specific to my particular setup

# new style
python import_customreport.py /Users/crc/Dropbox/Data/Education-Higher/IPEDS/custom_reports/prices.csv
python import_customreport.py /Users/crc/Dropbox/Data/Education-Higher/IPEDS/custom_reports/testscores.csv
python import_customreport.py /Users/crc/Dropbox/Data/Education-Higher/IPEDS/custom_reports/enrollment.csv
python import_customreport.py /Users/crc/Dropbox/Data/Education-Higher/IPEDS/custom_reports/grad_rates.csv

# old style auto-discover
python import_report.py /Users/crc/Dropbox/Data/Education-Higher/IPEDS/reports
