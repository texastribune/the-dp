MANAGE=python manage.py


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
	ENVIRONMENT=test $(MANAGE) test

# requires `postdoc`:
# pip install postdoc
dumpdb:
	phd pg_dump > tx_highered_$$(date +"%Y-%m-%d").sql

# this doesn't work quite right because syncdb tries to load fixtures
resetdb:
	$(MANAGE) reset_db --noinput
	$(MANAGE) syncdb --noinput
	$(MANAGE) migrate --noinput

