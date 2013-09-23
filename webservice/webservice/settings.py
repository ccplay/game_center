# Django settings for webservice p
# for django-cms
from os.path import join, dirname, abspath
gettext = lambda s: s
PROJECT_PATH = abspath(dirname(dirname(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-cn'
LANGUAGES_SUPPORTED = ('en', 'zh-cn',)

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
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = join(PROJECT_PATH, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&bfc%u6_w7)&r$(utbxk#!idnv*3bm^tqnc-lgrwq0=%lh@j7%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'webservice.middlewares.RequestFillLanguageCodeMiddleware',
)

ROOT_URLCONF = 'webservice.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'webservice.wsgi.application'

TEMPLATE_DIRS = (
    join(PROJECT_PATH, 'templates'),
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

INTERNAL_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'PIL',
    'easy_thumbnails',
    'south',
    'suit',
    'mptt',
    'reversion',
    'sizefield',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'webservice.Fix_PIL',
    'rest_framework',
    'rest_framework_swagger',
    'tagging',
    'tagging_autocomplete',
    'djrill',
]
EXTENDAL_APPS = [
    'mobapi',
    'searcher',
    'taxonomy',
    'warehouse'
]
INSTALLED_APPS = INTERNAL_APPS + EXTENDAL_APPS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LANGUAGES = (
    ('cn', gettext('Chinese')),
  #  ('en', gettext('English')),
)

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440*4
FILE_UPLOAD_PERMISSIONS = None
FILE_UPLOAD_TEMP_DIR = None

#from easy_thumbnails.conf import Settings as easy_thumbnails_defaults

THUMBNAIL_ALIASES = {
    '': {
        'screenshot_large': {'size':(412,232), 'crop':'smart'},
        'screenshot_preview': {'size':(412,232), 'crop':'smart'},
        'screenshot_thumbnail': {'size':(100,50), 'crop':'smart'},
        'avatar': {'size': (50, 50), 'crop': 'smart'},
        'icon': {'size': (72, 72)},
        },
    }
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    'easy_thumbnails.processors.filters',
)

REST_FRAMEWORK = {
    'DATE_FORMAT':'%s',
    'DATETIME_FORMAT':'%s',
    'PAGINATE_BY': 10,
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
}


#SLUGFIELD_SLUGIFY_FUNCTION = ''
TAGGING_AUTOCOMPLETE_JS_BASE_URL = '/media/js'
MANDRILL_API_KEY = "brack3t-is-awesome"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

SWAGGER_SETTINGS = {
    "exclude_namespaces": [], # List URL namespaces to ignore
    "api_version": '0.1', # Specify your API's version
    "enabled_methods": [ # Specify which methods to enable in Swagger UI
                         'get',
                         'post',
                         'put',
                         'patch',
                         'delete'
    ],
    "api_key": '', # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
}

def NOW():
    from django.utils import timezone
    return timezone.now()

