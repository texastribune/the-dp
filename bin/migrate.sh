cd ../exampleproject
# rm db.sqlite
dropdb thedp
createdb -T template_postgis thedp

python manage.py syncdb --noinput

# import
# python ../thedp/scripts/import_institutions.py
python manage.py loaddata fixtures/auth.json
