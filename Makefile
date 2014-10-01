# ignore warnings because they just fill the console with junk we don't care about
MANAGE=python -W ignore exampleproject/manage.py


help:
	@echo "make commands:"
	@echo "  make help    - this help"
	@echo "  make clean   - remove temporary files"
	@echo "  make test    - run test suite"
	@echo "  make dumpdb  - dump the SQL of current database to a timestamped file"
	@echo "  make resetdb - delete and recreate the database"


clean:
	find . -name "*.pyc" -delete
	find . -name ".DS_Store" -delete
	rm -rf MANIFEST
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info


test:
	ENVIRONMENT=test $(MANAGE) test test_tx_highered

# requires `postdoc`:
# pip install postdoc
dumpdb:
	phd pg_dump -Fc > $$(basename $$DATABASE_URL)_$$(date +"%Y-%m-%d").dump

# this doesn't work quite right because syncdb tries to load fixtures
# also see bin/migrate.sh
resetdb:
	$(MANAGE) reset_db --noinput
	$(MANAGE) syncdb --noinput --no-initial-data
	$(MANAGE) migrate --noinput
	# don't need initial data because it's in the tx_highered_2012 fixture
	# $(MANAGE) syncdb --noinput
	$(MANAGE) loaddata tx_highered_2012

# Dump current system and institution data into a fixture
.PHONY: tx_highered/fixtures/highered_base.json
tx_highered/fixtures/highered_base.json:
	$(MANAGE) dumpdata tx_highered.system tx_highered.institution > $@

# This is how I dumped old data to a fixture so I could work with the current
# data locally
.PHONY: tx_highered/fixtures/tx_highered_2012.json.gz
tx_highered/fixtures/tx_highered_2012.json.gz:
	$(MANAGE) dumpdata tx_highered | gzip > $@

# Load all the data
load: load_ipeds load_thecb

# Load IPEDS data
#
# Assumes data is in data/ipeds/*.csv
load_ipeds:
	find data/ipeds -name "*.csv" -print0 -exec $(MANAGE) tx_highered_import {} \;


# TODO make these all use management commands so can be done in integration project
load_thecb:
	@$(foreach file, $(wildcard data/*.csv), \
		echo $(file) && \
	  ./tx_highered/scripts/import_thecb_report.py $(file) && ) true
