cd $(cat $VIRTUAL_ENV/.project)/tx_highered/scripts

# I also have this in my virtualenv's postactivate
DJANGO_SETTINGS_MODULE=exampleproject.settings

# new style reports
python import_customreport.py $HOME/Dropbox/Data/Education-Higher/IPEDS/custom_reports/prices.csv
python import_customreport.py $HOME/Dropbox/Data/Education-Higher/IPEDS/custom_reports/testscores.csv
python import_customreport.py $HOME/Dropbox/Data/Education-Higher/IPEDS/custom_reports/enrollment.csv
python import_customreport.py $HOME/Dropbox/Data/Education-Higher/IPEDS/custom_reports/grad_rates.csv

# old style auto-discover
python import_report.py $HOME/Dropbox/Data/Education-Higher/IPEDS/reports
