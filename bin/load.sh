export PYTHONPATH=$(pwd)

# I also have this in my virtualenv's postactivate
export DJANGO_SETTINGS_MODULE=exampleproject.settings

# TODO don't setup examples here
export THEDP_IMPORT_LOGFILE="../../logs/logger.jslog"
mkdir -p ./logs

# new style reports
# ipeds
python tx_highered/scripts/import_customreport.py $HIGHER_ED_DATA/IPEDS/custom_reports/prices.csv
python tx_highered/scripts/import_customreport.py $HIGHER_ED_DATA/IPEDS/custom_reports/testscores.csv
python tx_highered/scripts/import_customreport.py $HIGHER_ED_DATA/IPEDS/custom_reports/enrollment.csv
python tx_highered/scripts/import_customreport.py $HIGHER_ED_DATA/IPEDS/custom_reports/grad_rates.csv
# thecb
python tx_highered/scripts/import_thecb_report.py $HIGHER_ED_DATA/THECB/custom_reports/top_10_percent.html

# old style auto-discover
python tx_highered/scripts/import_report.py $HIGHER_ED_DATA/IPEDS/reports
