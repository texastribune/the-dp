MANAGE=python exampleproject/manage.py


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
	ENVIRONMENT=test $(MANAGE) test tx_highered_test

# requires `postdoc`:
# pip install postdoc
dumpdb:
	phd pg_dump -Fc > $$(basename $$DATABASE_URL)_$$(date +"%Y-%m-%d").dump

# this doesn't work quite right because syncdb tries to load fixtures
# also see bin/migrate.sh
resetdb:
	$(MANAGE) reset_db --noinput
	$(MANAGE) syncdb --noinput
	$(MANAGE) migrate --noinput
