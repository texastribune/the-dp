# To generate the POST data, manually go to the $URL and make each of these
# reports. Then, using the network inspector, copy the POST data.
URL=http://www.txhighereddata.org/Interactive/Accountability/InteractiveGenerate.cfm
#
# Other potential data sources:
#
# PREP: http://www.txhighereddata.org/Interactive/PREP_New/
# Has enrollment, degrees awarded, declared majors, semester credit hours,
# and contact hours
#
# txhigherdata.org Has Admissions data in PDF. Click the
# "Applicants/Acceptance/Enrollment" link to go to
# http://www.txhighereddata.org/index.cfm?objectId=27282A55-A77E-2A0D-87B58BE320C6B099
# which lets you download a pdf by year, starting from 1998

all: top_10_percent \
	graduation_rate_four \
	graduation_rate_five \
	graduation_rate_six


# Participation /Contextual Measures / First-Time Students in Top 10%
#
# THECB is missing 2001 because they didn't start doing data entry until 2004
# and they haven't gotten around to importing all old data
top_10_percent:
	curl -X POST ${URL} --data-binary "@thecb/$@.POST" > thecb/$@.xls.html
	../tx_highered/thecb_importer/html_to_csv.py thecb/$@.xls.html > thecb/$@.csv

# Participation / Key Measures / Full-Time Equivalent Enrollment / Total FTE
total_fte:
	curl -X POST ${URL} --data-binary "@thecb/$@.POST" > thecb/$@.xls.html
	../tx_highered/thecb_importer/html_to_csv.py thecb/$@.xls.html > thecb/$@.csv

# Success / Key Measures / Four-Year Graduation Rate / Percent Total
graduation_rate_four:
	curl -X POST ${URL} --data-binary "@thecb/$@.POST" > thecb/$@.xls.html
	../tx_highered/thecb_importer/html_to_csv.py thecb/$@.xls.html > thecb/$@.csv

# Success / Key Measures / Five-Year Graduation Rate / Percent Total
graduation_rate_five:
	curl -X POST ${URL} --data-binary "@thecb/$@.POST" > thecb/$@.xls.html
	../tx_highered/thecb_importer/html_to_csv.py thecb/$@.xls.html > thecb/$@.csv

# Success / Key Measures / Six-Year Graduation Rate / Percent Total
graduation_rate_six:
	curl -X POST ${URL} --data-binary "@thecb/$@.POST" > thecb/$@.xls.html
	../tx_highered/thecb_importer/html_to_csv.py thecb/$@.xls.html > thecb/$@.csv


# Community Colleges

# Participation / Key Measures / Full-Time Equivalent Enrollment / Total FTE
# TODO I can't find full time equivalent, only part time and full time
community_total_fte:
	curl -X POST ${URL} --data-binary "@thecb/$@.POST" > thecb/$@.xls.html
	../tx_highered/thecb_importer/html_to_csv.py thecb/$@.xls.html > thecb/$@.csv

# Success / Key Measures / Three-Year Graduation Rate / Associates
# Success / Key Measures / Three-Year Graduation Rate / Bachelors
# Success / Key Measures / Four-Year Graduation Rate / Associates
# Success / Key Measures / Four-Year Graduation Rate / Bachelors
# Success / Key Measures / Six-Year Graduation Rate / Associates
# Success / Key Measures / Six-Year Graduation Rate / Bachelors
#
# No Five-Year data from Accountability reports for Community colleges
# Years 2001 to 2003 are missing
community_graduation_rates:
	curl -X POST ${URL} --data-binary "@thecb/$@.POST" > thecb/$@.xls.html
	../tx_highered/thecb_importer/html_to_csv.py thecb/$@.xls.html > thecb/$@.csv
