cd $(cat $VIRTUAL_ENV/.project)/exampleproject

# export data about institutions
python manage.py dumpdata tx_highered.system tx_highered.institution --indent 2 > ../tx_highered/fixtures/initial_data.json
# export saved IPEDS variables
python manage.py dumpdata ipeds_importer --indent 2 > ../tx_highered/ipeds_importer/fixtures/initial_data.json
