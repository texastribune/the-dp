from fabric.api import local, task

import os

import dj_database_url


def get_production_db():
    out = local("heroku config:get DATABASE_URL", capture=True)
    return dj_database_url.parse(out)


def get_local_db():
    return dj_database_url.parse('postgis:///tx_highered')  # TODO magic string


def generate_dump_cmd(db):
    string = "pg_dump -Fc --no-acl --no-owner -t \"tx_highered*\" -w"
    if db['HOST']:
        string += " -h %s" % db['HOST']
    if db['USER']:
        string += " -U %s" % db['USER']
    if db['PASSWORD']:
        string = "PGPASSWORD=%s %s" % (db['PASSWORD'], string)
    # TODO db['PORT']
    string += " " + db['NAME']
    return string


def generate_restore_cmd(db, fn):
    string = "pg_restore --clean --no-acl --no-owner -d %s" % db['NAME']
    if db['HOST']:
        string += " -h %s" % db['HOST']
    if db['USER']:
        string += " -U %s" % db['USER']
    if db['PASSWORD']:
        string = "PGPASSWORD=%s %s" % (db['PASSWORD'], string)
    string += " %s" % fn
    return string


@task
def dbpush(fn):
    """ Push local db into `file` and then into production db """
    local(generate_dump_cmd(get_production_db()) + " > " + fn + ".backup")
    local(generate_dump_cmd(get_local_db()) + " > " + fn)
    if os.path.isfile(fn):
        local(generate_restore_cmd(get_production_db(), fn))


@task
def dbpull(fn):
    """ Pull production db into `file` """
    local(generate_dump_cmd(get_production_db()) + " > " + fn)
