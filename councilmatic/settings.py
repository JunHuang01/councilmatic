import os
try:
    from application_keys import councilmatic_keys
except ImportError:
    from os import environ as councilmatic_keys


# Make filepaths relative to settings.
def rel_path(*subs):
    """Make filepaths relative to this settings file"""
    root_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root_path, *subs)


###############################################################################
#
# Platform-specific values
#

# If the environment is DotCloud...
if os.path.exists('/home/dotcloud/current'):
    import json
    with open("/home/dotcloud/environment.json") as env_json:
        env = json.load(env_json)

        DB_ENGINE = 'postgis'
        DB_NAME = 'councilmatic'
        DB_HOST = env['DOTCLOUD_DB_SQL_HOST']
        DB_USER = env['DOTCLOUD_DB_SQL_LOGIN']
        DB_PASSWORD = env['DOTCLOUD_DB_SQL_PASSWORD']
        DB_PORT = env['DOTCLOUD_DB_SQL_PORT']
        WHOOSH_PATH = '/home/dotcloud/whoosh_index'
        LOGFILE_PATH= '/home/dotcloud/logs/councilmatic.log'

# Otherwise, if it's dev...
else:
    DB_ENGINE = 'postgis'
    DB_NAME = 'councilmatic'
    DB_HOST = ''
    DB_USER = 'councilmatic'
    DB_PASSWORD = 'councilmatic'
    DB_PORT = ''
    WHOOSH_PATH = rel_path('whoosh_index')
    LOGFILE_PATH= rel_path('logs/councilmatic.log')


# Django settings for councilmatic project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.' + DB_ENGINE, # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DB_NAME,                      # Or path to database file if using sqlite3.
        'USER': DB_USER,                      # Not used with sqlite3.
        'PASSWORD': DB_PASSWORD,                  # Not used with sqlite3.
        'HOST': DB_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': DB_PORT,                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = rel_path('..', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    rel_path('static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j#gwlh#fyt$v-l144lw7*8ybmosn8gxo_b5tk+l2wffwr+n=s)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'utils.context_processors.settings.GOOGLE_ANALYTICS_ACCOUNT',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates". Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    rel_path('phillyleg'),
    rel_path('templates'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

###############################################################################
#
# Authentication
#

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/login/error'

###############################################################################
#
# 3rd-party service configuration and keys
#

cmk = councilmatic_keys

TWITTER_CONSUMER_KEY         = cmk.get('TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET      = cmk.get('TWITTER_CONSUMER_SECRET', '')
FACEBOOK_APP_ID              = cmk.get('FACEBOOK_APP_ID', '')
FACEBOOK_API_SECRET          = cmk.get('FACEBOOK_API_SECRET', '')
LINKEDIN_CONSUMER_KEY        = cmk.get('LINKEDIN_CONSUMER_KEY', '')
LINKEDIN_CONSUMER_SECRET     = cmk.get('LINKEDIN_CONSUMER_SECRET', '')
GOOGLE_CONSUMER_KEY          = cmk.get('GOOGLE_CONSUMER_KEY', '')
GOOGLE_CONSUMER_SECRET       = cmk.get('GOOGLE_CONSUMER_SECRET', '')

RECAPTCHA_PUBLIC_KEY  = cmk.get('RECAPTCHA_PUBLIC_KEY', '')
RECAPTCHA_PRIVATE_KEY = cmk.get('RECAPTCHA_PRIVATE_KEY', '')

GOOGLE_ANALYTICS_ACCOUNT = cmk.get('GOOGLE_ANALYTICS_ACCOUNT', '')

###############################################################################
#
# Site search configuration
#

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_PATH,
    }
}

# There were some queries that were taking waaaaaay too long (as in, timing
# out in production) because there were too many results.  In short, to "fix",
# I found this: https://github.com/toastdriven/django-haystack/issues/159
#
# I can't set this too high though, or I'll get a "Too many SQL variables"
# error; i.e., http://stackoverflow.com/questions/7106016/too-many-sql-variables-error-in-django-witih-sqlite3
HAYSTACK_ITERATOR_LOAD_PER_QUERY = 800

###############################################################################
#
# Applications
#

COMMUNITY_APPS = (
    'registration',
    'captcha',
    'south',
    'haystack',
    'uni_form',
    'django_nose',
    'debug_toolbar',
    'social_auth',
    'ebdata', # From everyblock -- used here for parsing addresses and such
    'compressor',
    'djangorestframework',
)

MY_REUSABLE_APPS = (
   'model_blocks',
   'mustachejs',
)

PROJECT_APPS = (
    'cm',
    'cm_api',
    'phillyleg',
    'subscriptions',
    'bookmarks',
    'activity_log',
    'opinions',
    'main',
    'utils',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.gis',
) + COMMUNITY_APPS + MY_REUSABLE_APPS + PROJECT_APPS

################################################################################
#
# Testing and administration
#

# Tests (nose)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False

# Debug toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}
INTERNAL_IPS = ('127.0.0.1',)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'filters': {
    },

    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter':'verbose',
        },
        'logfile':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':LOGFILE_PATH,
            'formatter':'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },

    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['logfile', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        'councilmatic': {
            'handlers': ['console', 'logfile', 'mail_admins'],
            'level': 'DEBUG',
        },
        'phillyleg.management': {
            'handlers': ['console', 'logfile', 'mail_admins'],
            'level': 'DEBUG',
        },
    }
}
