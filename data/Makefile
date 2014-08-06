URL=http://www.txhighereddata.org/Interactive/Accountability/InteractiveGenerate.cfm


.PHONY: community_graduation_rates.xls.html
community_graduation_rates.xls.html:
	curl -X POST ${URL} --data-binary "@community_graduation_rates.POST" > $@

.PHONY: enrollment_fte.xls.html
enrollment_fte.xls.html:
	curl -X POST ${URL} --data-binary "@enrollment_fte.POST" > $@

.PHONY: state_graduation_rates.xls.html
state_graduation_rates.xls.html:
	curl -X POST ${URL} --data-binary "@state_graduation_rates.POST" > $@

.PHONY: top_10_percent.xls.html
top_10_percent.xls.html:
	curl -X POST ${URL} --data-binary "@top_10_percent.POST" > $@

.PHONY: university_graduation_rates.xls.html
university_graduation_rates.xls.html:
	curl -X POST ${URL} --data-binary "@university_graduation_rates.POST" > $@
