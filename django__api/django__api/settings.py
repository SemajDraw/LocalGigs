import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.name == 'nt':
    from distutils.sysconfig import get_python_lib
    os.environ["PATH"] += os.pathsep + get_python_lib() + '\\osgeo'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'oda-f9%zg@%g+*c05bhv_hhv=7-@2102)365)f*6t+m7fhbx@&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.sites',
    'django_extensions',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'social_django',

    'rest_auth',
    'rest_auth.registration',

    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',

    'requests',
    'crispy_forms',
    'leaflet',
    'bootstrap3',
    'ticketpy',
    'sslserver',
    'corsheaders',

    'app.apps.AppConfig',
    'api',
]

SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'django__api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'templates', 'allauth')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

ACCOUNT_SIGNUP_FORM_CLASS = 'app.forms.SignupForm'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.spotify.SpotifyOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',

)


# Django social auth SPOTIFY
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_SPOTIFY_KEY = '6cb146053e70453eb4a745a93dcfe480'
SOCIAL_AUTH_SPOTIFY_SECRET = 'a6a8705f1436458288f53e273c27218b'
SOCIAL_AUTH_SPOTIFY_SCOPE = ['user-read-private playlist-read-private user-top-read user-read-email']

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)


# Django social account FACEBOOK
SOCIALACCOUNT_QUERY_EMAIL = True

ACCOUNT_EMAIL_REQUIRED = True

SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
        {'METHOD': 'oauth2',
            'SCOPE': ['email', 'public_profile', 'user_friends'],
            'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
            'FIELDS': [
                'id',
                'email',
                'name',
                'first_name',
                'last_name',
                'verified',
                'locale',
                'timezone',
                'link',
                'gender',
                'updated_time'],
            'EXCHANGE_TOKEN': True,
            'LOCALE_FUNC': lambda request: 'kr_KR',
            'VERIFIED_EMAIL': False,
            'VERSION': 'v2.4'}
     }

WSGI_APPLICATION = 'django__api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gigDB',
        'USER': 'james',
        'HOST': 'gig-db.cy4vlh07jpj5.eu-west-1.rds.amazonaws.com',
        'PASSWORD': 'Ibanezrg320dx',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/user/profile_images')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

REST_AUTH_REGISTER_SERIALIZERS = {
        'REGISTER_SERIALIZER': 'api.serializers.RegisterSerializer',
}

LEAFLET_CONFIG = {
    'DEFAULT_ZOOM': 14,
    'MIN_ZOOM': 1,
    'MAX_ZOOM': 18,

    'PLUGINS': {
        'routing': {
            'css': 'https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.css',
            'js': 'https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.js',
            'auto-include': True,
        },
    }
}

LOGIN_REDIRECT_URL = '/home/'

CORS_ORIGIN_ALLOW_ALL = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TM_APP_KEY = "YogbcbgUOqYjSxOcy5YMOzwS6zvv8LAM"

TM_REC_KEY = "W5CYYvcnTtYhxj5xicjAPMq0IF4A3MFu"

GEOIP_PATH = os.path.join(BASE_DIR, 'GeoLite2/GeoLite2-City_20190312')

# # Process background tasks in parallel
# BACKGROUND_TASK_RUN_ASYNC = True
