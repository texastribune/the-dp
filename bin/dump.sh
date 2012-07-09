cd ../exampleproject
python manage.py dumpdata tx_highered.system tx_highered.institution --indent 2 > ../tx_highered/fixtures/initial_data.json
python manage.py dumpdata ipeds_importer --indent 2 > ../ipeds_importer/fixtures/initial_data.json
