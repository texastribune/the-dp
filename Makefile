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
	$(MANAGE) syncdb --noinput
	$(MANAGE) loaddata tx_highered_2012

# Dump current system and institution data into a fixture
.PHONY: tx_highered/fixtures/highered_base.json
tx_highered/fixtures/highered_base.json:
	$(MANAGE) dumpdata tx_highered.system tx_highered.institution > $@

# Load all the data
#
# This functionality could all just live in this makefile, but make does not
# like file names containing spaces, and browsers will create files names with
# spaces. So :shrug:
load:
	bin/load.sh
