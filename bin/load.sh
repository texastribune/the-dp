DJANGO_SETTINGS_MODULE=exampleproject.settings
cd ../tx_highered/scripts/

# These locations are specific to my particular setup

# new style
python import_customreport.py prices /Users/crc/Dropbox/Data/Education-Higher/IPEDS/custom_reports/price.csv
python import_customreport.py testscores /Users/crc/Dropbox/Data/Education-Higher/IPEDS/custom_reports/testscores.csv

# old style auto-discover
python import_report.py /Users/crc/Dropbox/Data/Education-Higher/IPEDS/reports
