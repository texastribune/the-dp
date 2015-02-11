# ignore warnings because they just fill the console with junk we don't care about
MANAGE=python -W ignore exampleproject/manage.py
VERSION=0.3.3

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
	DJANGO_SETTINGS_MODULE=exampleproject.settings ENVIRONMENT=test $(MANAGE) test test_tx_highered --noinput

# requires `postdoc`:
# pip install postdoc
dumpdb:
	phd pg_dump -Fc > $$(basename $$DATABASE_URL)_$$(date +"%Y-%m-%d").dump

# delete and re-create your entire database
# TODO should I just sqlclear | dbshell instead since there's only one app?
resetdb:
	$(MANAGE) reset_db --noinput

# bring database up to speed
syncdb:
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
	find data/ipeds -name "*.csv" -print0 -exec $(MANAGE) tx_highered_import ipeds {} \;


# Load THECB data
#
# Assumes data is in data/*.csv
load_thecb:
	@$(foreach file, $(wildcard data/thecb/*.csv), \
		echo $(file) && \
	  $(MANAGE) tx_highered_import thecb $(file) && ) true
	python tx_highered/thecb_importer/load_enrollment.py


version:
	@sed -i -r /version/s/[0-9.]+/$(VERSION)/ setup.py
	@sed -i -r /version/s/[0-9.]+/$(VERSION)/ tx_highered/__init__.py


# Release Instructions:
#
# 1. bump version number at the top of this file
# 2. `make release`
release: clean version
	@-git commit -am "bump version to v$(VERSION)"
	@-git tag v$(VERSION)
	@-pip install wheel > /dev/null
	python setup.py sdist bdist_wheel upload
