from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ronz*&0zfhi5y5f-+3hfpm&ae+z_n+t4q0!l+gua-wfv#oey(m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'venue-connect-092139c4b592.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'phonenumber_field',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    # Deployment only
    'corsheaders',
    # Local apps
    'users',
    'venues'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
if IS_HEROKU_APP:
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        ),
    }
else:
    # DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'venueconnect',
    #     'USER': 'vcadmin',
    #     'PASSWORD': 'venueconnect@2024',
    #     'HOST': 'localhost',
    #     'PORT': '',
    # }
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dgmes10sn26bs',
        'USER': 'qtcjyedwtcqhdk',
        'PASSWORD': 'bfbb095427a307ac30a3f9b031cf2b6e9895378dd19b8b251af20c355b2e0e29',
        'HOST': 'ec2-54-144-112-84.compute-1.amazonaws.com',
        'PORT': '5432',
        'NAME': 'dgmes10sn26bs',
        'USER': 'qtcjyedwtcqhdk',
        'PASSWORD': 'bfbb095427a307ac30a3f9b031cf2b6e9895378dd19b8b251af20c355b2e0e29',
        'HOST': 'ec2-54-144-112-84.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# For meadia 
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

AUTH_USER_MODEL = "users.CustomUser"

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        }
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ALLOW_ALL_ORIGINS = True

# Persistent storage (Cloud Cube S3 amazonaws)
if IS_HEROKU_APP:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    cloudcube_url = os.environ.get('CLOUDCUBE_URL')
    cloudcube_bucket = os.path.basename(cloudcube_url)
    cloudcube_base_url = os.path.dirname(cloudcube_url)

    AWS_S3_ENDPOINT_URL = cloudcube_base_url
    AWS_ACCESS_KEY_ID = os.environ.get('CLOUDCUBE_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('CLOUDCUBE_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = cloudcube_bucket
    AWS_DEFAULT_ACL = os.environ.get('AWS_DEFAULT_ACL', 'public-read')
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_SIGNATURE_VERSION = "s3v4"