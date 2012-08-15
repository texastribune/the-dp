cd $(cat $VIRTUAL_ENV/.project)/tx_highered/scripts

# I also have this in my virtualenv's postactivate
DJANGO_SETTINGS_MODULE=exampleproject.settings

# TODO don't setup examples here
export THEDP_IMPORT_LOGFILE="../../logs/logger.jslog"
mkdir -p ../../logs

# new style reports
# ipeds
python import_customreport.py $HIGHER_ED_DATA/IPEDS/custom_reports/prices.csv
python import_customreport.py $HIGHER_ED_DATA/IPEDS/custom_reports/testscores.csv
python import_customreport.py $HIGHER_ED_DATA/IPEDS/custom_reports/enrollment.csv
python import_customreport.py $HIGHER_ED_DATA/IPEDS/custom_reports/grad_rates.csv
# thecb
./import_thecb_report.py $HIGHER_ED_DATA/THECB/custom_reports/top_10_percent.html

# old style auto-discover
python import_report.py $HIGHER_ED_DATA/IPEDS/reports
