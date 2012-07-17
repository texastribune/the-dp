cd $(cat $VIRTUAL_ENV/.project)/exampleproject

# rm db.sqlite
dropdb tx_highered
createdb -T template_postgis tx_highered

python manage.py syncdb --noinput

# import
# python ../tx_highered/scripts/import_institutions.py
python manage.py loaddata fixtures/auth.json
