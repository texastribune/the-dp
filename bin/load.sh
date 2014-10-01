#!/usr/bin/env bash

set -e

export PYTHONPATH=$(pwd)

# Make sure you have these environment variables and directories set:
# export DJANGO_SETTINGS_MODULE=exampleproject.settings
# export HIGHER_ED_DATA=$HOME/Download/Data

# IPEDS
for file in $HIGHER_ED_DATA/*.csv; do
  echo "Processing ${file}"
  python tx_highered/scripts/import_customreport.py ${file}
done

# thecb
# TODO get these working again too
# TODO make it so the directory structure doesn't matter for ipeds/thecb csvs
# python tx_highered/scripts/import_thecb_report.py $HIGHER_ED_DATA/THECB/custom_reports/top_10_percent.html
# python tx_highered/thecb_importer/load_enrollment.py
