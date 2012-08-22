export PYTHONPATH=.

# sync the configured database
python exampleproject/manage.py syncdb --noinput
python exampleproject/manage.py migrate

# add the user: admin/admin
python exampleproject/manage.py loaddata ./exampleproject/fixtures/auth.json
# for some reason syncdb doesn't pick this up
python exampleproject/manage.py loaddata ./exampleproject/fixtures/initial_data.json

# since this is a new database, delete any old log files if they exist
# TODO don't setup examples here
export THEDP_IMPORT_LOGFILE="./logs/logger.jslog"
if [ -f $THEDP_IMPORT_LOGFILE ]; then
	rm $THEDP_IMPORT_LOGFILE
fi
