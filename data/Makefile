# To generate the POST data, manually go to the $URL and make each of these
# reports. Then, using the network inspector, copy the POST data.
URL=http://www.txhighereddata.org/Interactive/Accountability/InteractiveGenerate.cfm

all: top_10_percent.xls.html total_fte.xls.html \
	graduation_rate_four \
	graduation_rate_five \
	graduation_rate_six


.PHONY: community_graduation_rates.xls.html
community_graduation_rates.xls.html:
	curl -X POST ${URL} --data-binary "@community_graduation_rates.POST" > $@


# Participation / Key Measures / Contextual Measures / First-Time Students in Top 10%
#
# THECB is missing 2001 because they didn't start doing data entry until 2004
# and they haven't gotten around to importing all old data
.PHONY: top_10_percent.xls.html
top_10_percent.xls.html:
	curl -X POST ${URL} --data-binary "@top_10_percent.POST" > $@

# Participation / Key Measures / Full-Time Equivalent Enrollment / Total FTE
.PHONY: total_fte.xls.html
total_fte.xls.html:
	curl -X POST ${URL} --data-binary "@total_fte.POST" > $@

# Success / Key Measures / Four-Year Graduation Rate / Percent Total
graduation_rate_four:
	curl -X POST ${URL} --data-binary "@$@.POST" > $@.xls.html
	../tx_highered/thecb_importer/html_to_csv.py $@.xls.html > $@.csv

# Success / Key Measures / Five-Year Graduation Rate / Percent Total
graduation_rate_five:
	curl -X POST ${URL} --data-binary "@$@.POST" > $@.xls.html
	../tx_highered/thecb_importer/html_to_csv.py $@.xls.html > $@.csv

# Success / Key Measures / Six-Year Graduation Rate / Percent Total
graduation_rate_six:
	curl -X POST ${URL} --data-binary "@$@.POST" > $@.xls.html
	../tx_highered/thecb_importer/html_to_csv.py $@.xls.html > $@.csv
