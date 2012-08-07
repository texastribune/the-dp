The Texas Higher Education Data Project
---------------------------------------

A Very Rough guide to starting devlopment:
# install postgresql libpq-dev

git checkout $REPOSITORY && cd $PATH
mkvirtualenv $ENVNAME
setvirtualenvproject
pip install -r requirements-dev.txt
export DJANGO_SETTINGS_MODULE=exampleproject.settings
add2virtualenv .

# syncdb and load fixtures
./bin/migrate.sh

# load raw data
./bin/load.sh


Getting Data from the Texas Higher Education Coordinating Board
------------------
If you want to regrab data from THECB's web site, first find the data file that you want to re-grab.
It will be named something like "top_10_percent.html". There will also be a file called "top_10_percent.POST". From that file you can recreate the report with the command:

    curl -X POST -d @top_10_percent.POST http://www.txhighereddata.org/interactive/accountability/InteractiveGenerate.cfm -s -v > blahblahblah.html

If you need to modify the report, you can reverse engineer it from the POST data and the form markup.




(c) 2012 The Texas Tribune
