import os

from project_runpy import env
import dj_database_url


# From armstrong.cli. This function will eventually be in an armstrong
# utils package, at which point we should stop duplicating it here.
def project_dir(*paths):
    base = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(base, *paths)

DEBUG = env.get('DEBUG', True)  # example project, so assume you're debugging
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config(default='postgis:///tx_highered')}
DATABASES['default']['OPTIONS'] = {'autocommit': True}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_NAME = "THEDP"
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = project_dir('media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'test!kskf-4=)f_tbn$scxdfmg%17wetw@1iu%$=0sy0k@33oh)x9e'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'exampleproject.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'exampleproject.wsgi.application'

TEMPLATE_DIRS = (
    project_dir('templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.gis',

    'django_object_actions',

    # app
    'tx_lege_districts',
    'tx_highered',
    'tx_highered.instachart',

    # Here for loading the test data
    'exampleproject.test_tx_highered',
]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)


# for Heroku support
if 'GEOS_LIBRARY_PATH' in env:
    GEOS_LIBRARY_PATH = env.get('GEOS_LIBRARY_PATH')
    GDAL_LIBRARY_PATH = env.get('GDAL_LIBRARY_PATH')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': os.environ.get('LOGGING_LEVEL', 'WARNING'),
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': ' '.join([
                '%(levelname)s',
                '%(asctime)s',
                '%(name)s',
                '%(module)s',
                '%(process)d',
                '%(thread)d',
                '%(message)s']),
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'readable_sql': {
            '()': 'project_runpy.ReadableSqlFilter',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'project_runpy.ColorizingStreamHandler',
        },
    },
    'loggers': {
        'py.warnings': {
            # how do i get colored warnings without duplicates?
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'DEBUG' if env.get('SQL') else 'INFO',
            'filters': ['require_debug_true', 'readable_sql'],
            'propagate': False,
        },
        'factory': {
            'level': 'ERROR',
            'propagate': False,
        },
        'south': {
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
