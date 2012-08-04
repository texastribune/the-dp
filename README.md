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


(c) 2012 The Texas Tribune
