from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



def verified_callback(user):
    user.is_active = True

# for email setting
EMAIL_VERIFIED_CALLBACK = verified_callback
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_FROM_ADDRESS = 'testadarsha5@gmail.com'
EMAIL_PASSWORD = 'nepali**--te'
EMAIL_ADDRESS = 'testadarsha5@gmail.com'
EMAIL_ACTIVE_FIELD = 'is_active'
EMAIL_PAGE_DOMAIN = 'http://127.0.0.1:8000/'
EMAIL_MAIL_SUBJECT = 'Confirm your email'
EMAIL_MAIL_HTML = 'testt.html'
EMAIL_PAGE_TEMPLATE='Response.html'

#  for sending email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'testadarsha5@gmail.com'
EMAIL_HOST_PASSWORD = 'nepali**--te'
EMAIL_TOKEN_LIFE = 60 * 60
#




# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w-+(1*zk=qrwr6hzt@(54%#^hlk7-2l*rf^6&vxq9b0r7n-ysl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# session time
SESSION_COOKIE_AGE = 3600
#  1 hour

# Application definition


INSTALLED_APPS = [
    'channels',
    'messagingsystem',
    'django.contrib.admin',
    'django.contrib.auth',
    'verify_email',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # for static files
    'django_sass', # scss
    'UserManagementSystem',  # app
    'PostManagementSystem',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# for email backend production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# for testing  djano..............console.Emailbackend

ROOT_URLCONF = 'MeroAgro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['MeroAgro/templates',
                 'UserManagementSystem/templates',
                 'PostManagementSystem/templates'],
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

WSGI_APPLICATION = 'MeroAgro.wsgi.application'
ASGI_APPLICATION  = 'MeroAgro.asgi.application'

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }


# also for testing immem channel layers
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}




# Database

# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS=(
    os.path.join(BASE_DIR,'static'),
)

#  default storage system
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/'

STATIC_ROOT = '/static'