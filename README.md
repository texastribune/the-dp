The Texas Higher Education Data Project
---------------------------------------

A Very Rough guide to starting devlopment:

Your `.env` file:

```
DJANGO_SETTINGS_MODULE=exampleproject.settings.dev
DATABASE_URL=postgis:///tx_highered
HIGHER_ED_DATA=~/Dropbox/Data/Education-Higher
```

Getting started:

```bash
# install postgresql libpq-dev

git clone $REPOSITORY && cd $PATH
mkvirtualenv tx_higher_ed
setvirtualenvproject
add2virtualenv .
pip install -r requirements.txt

# syncdb and load fixtures
make resetdb
make syncdb

# if using 2012 data, bump it up to 2014 standards
python tx_highered/scripts/2014_update.py

# get ipeds data, requires https://github.com/texastribune/ipeds_reporter
../ipeds_reporter/csv_downloader/csv_downloader.py \
  --uid data/ipeds/ipeds_institutions.uid --mvl data/ipeds
mv ~/Downloads/Data_*.csv data/ipeds
# get thecb data
cd data && make all
# load data
#   timing: 3m38.666s
make load
# post-process the data
django tx_highered_process
```

Database:

This project currently requires a PostGIS database (hopefully not for long):

```bash
$ phd createdb
$ phd psql

CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
```

Getting Data from the IPEDS Data Center
-----------------
When it asks you for an Institution, enter a list of UnitIDs generated by:

	list(Institution.objects.filter(ipeds_id__isnull=False).values_list('ipeds_id', flat=True))

Getting Data from the Texas Higher Education Coordinating Board
------------------
If you want to regrab data from THECB's web site, first find the data file that you want to re-grab.
It will be named something like "top_10_percent.html". There will also be a file called "top_10_percent.POST". From that file you can recreate the report with the command:

    curl -X POST -d @top_10_percent.POST http://www.txhighereddata.org/interactive/accountability/InteractiveGenerate.cfm -s -v > blahblahblah.html

If you need to modify the report, you can reverse engineer it from the POST data and the form markup.




(c) 2012 The Texas Tribune
