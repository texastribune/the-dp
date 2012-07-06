cd ../exampleproject
python manage.py dumpdata tx_highered.system tx_highered.institution --indent 2 > ../tx_highered/fixtures/initial_data.json
