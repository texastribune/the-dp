export PYTHONPATH=.

# rm db.sqlite
dropdb tx_highered
# createdb -T template_postgis tx_highered
createdb tx_highered

python exampleproject/manage.py syncdb --noinput

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
