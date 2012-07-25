cd $(cat $VIRTUAL_ENV/.project)/exampleproject

# rm db.sqlite
dropdb tx_highered
# createdb -T template_postgis tx_highered
createdb tx_highered

python manage.py syncdb --noinput

# add the user: admin/admin
python manage.py loaddata fixtures/auth.json
