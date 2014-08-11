#!/usr/bin/env bash

set -e

export PYTHONPATH=$(pwd)

# Make sure you have these environment variables and directories set:
# export DJANGO_SETTINGS_MODULE=exampleproject.settings
# export HIGHER_ED_DATA=$HOME/Download/Data
# export THEDP_IMPORT_LOGFILE="../../logs/logger.jslog"
# mkdir -p ./logs

# ipeds
#   new style reports
python tx_highered/scripts/import_customreport.py $HIGHER_ED_DATA/IPEDS/custom_reports/prices.csv
python tx_highered/scripts/import_customreport.py $HIGHER_ED_DATA/IPEDS/custom_reports/testscores.csv
python tx_highered/scripts/import_customreport.py $HIGHER_ED_DATA/IPEDS/custom_reports/enrollment.csv
python tx_highered/scripts/import_customreport.py $HIGHER_ED_DATA/IPEDS/custom_reports/grad_rates.csv
#   old style auto-discover
python tx_highered/scripts/import_report.py $HIGHER_ED_DATA/IPEDS/reports

# thecb
python tx_highered/scripts/import_thecb_report.py $HIGHER_ED_DATA/THECB/custom_reports/top_10_percent.html
python tx_highered/thecb_importer/load_enrollment.py
python tx_highered/thecb_importer/load_graduation_rates.py $HIGHER_ED_DATA/THECB/custom_reports/university_graduation_rates.xls.html
python tx_highered/thecb_importer/load_graduation_rates.py $HIGHER_ED_DATA/THECB/custom_reports/community_graduation_rates.xls.html
python tx_highered/thecb_importer/load_graduation_rates.py $HIGHER_ED_DATA/THECB/custom_reports/state_graduation_rates.xls.html
python tx_highered/thecb_importer/load_almanac_graduation_rates.py $HIGHER_ED_DATA/THECB/Almanac/almanac_p21.pdf.json
python tx_highered/thecb_importer/load_admissions.py $HIGHER_ED_DATA/THECB/Admissions/
echo "Done!"
