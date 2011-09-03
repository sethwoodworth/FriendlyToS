import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Seth Woodworth', 'seth@sethish.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Sqlite during development, replace.
        'ENGINE': 'django.db.backends.sqlite',
        'NAME': 'temp.sql',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'America/Detroit'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False # no translations yet
USE_L10N = True  # localizes dates

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../media/')
MEDIA_URL = 'media/' # Not likely to use user media, but just in case

STATIC_ROOT = os.path.join(os.path.dirname(__file__), './static/')
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), '../static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# TODO: Deploy with a new key
SECRET_KEY = '@n_$a0rr@^yk!wb+uy_mneh_kk(wf^w*)io15j=9kmuzbnryov'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'frndlyts.urls'

TEMPLATE_DIRS = (
    # Wherever you go, there you are
    os.path.join(os.path.dirname(__file__), 'templates'),
)

## ---- start: Userena ---- ##
AUTH_PROFILE_MODULE = 'tosview.UserProfile'
ANONYMOUS_USER_ID   = -1
LOGIN_REDIRECT_URL  = '/dashboard/'
USERENA_SIGNIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL           = '/accounts/signin/'
LOGOUT_URL          = '/accounts/signout/'
USERENA_DEFAULT_PRIVACY = 'closed'

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

## ---- end: Userena   ---- ##

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # Userena
    'guardian',
    'easy_thumbnails',
    'userena',

    # Local apps
    'tosview',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from local_settings import *
except:
    pass
