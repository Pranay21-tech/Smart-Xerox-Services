from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8s_a%$bt1l1cx=so9d9@xzvg3u^+si!hp8nwpqf^w+edzmx61&'
# SECRET_KEY = os.environ.get('django-insecure-8s_a%$bt1l1cx=so9d9@xzvg3u^+si!hp8nwpqf^w+edzmx61&')

DEBUG = True

ALLOWED_HOSTS = ['*']


# ======================
# INSTALLED APPS
# ======================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    "rest_framework",
    "rest_framework.authtoken",

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'social_django',

    'smartxerox',
]

SITE_ID = 1


# ======================
# MIDDLEWARE
# ======================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'allauth.account.middleware.AccountMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


ROOT_URLCONF = 'backend.urls'


# ======================
# TEMPLATES
# ======================

TEMPLATES = [
{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'smartxerox', 'templates')],  # 🔥 FIX
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


WSGI_APPLICATION = 'backend.wsgi.application'


# ======================
# DATABASE
# ======================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# MongoDB connection
from mongoengine import connect

connect(
    db="smartxeroxservice26",
    host="mongodb+srv://smartxeroxservice26:smartxeroxservice26@smart-xerox-service.ets6zxt.mongodb.net/"
)


# ======================
# SESSION
# ======================

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


# ======================
# AUTHENTICATION
# ======================

AUTHENTICATION_BACKENDS = (
     'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/main/'
LOGOUT_REDIRECT_URL = '/'


# ======================
# GOOGLE OAUTH
# ======================

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "899444823284-comtell9c1no1fqbsaukkoeump0pb1hk.apps.googleusercontent.com"

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/main/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login/'

SOCIAL_AUTH_ASSOCIATE_BY_EMAIL = True
SOCIAL_AUTH_EMAIL_AUTHENTICATION_AUTO_ASSOCIATE = True


# ======================
# SOCIAL AUTH PIPELINE
# ======================

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',

    # save email in session
    'smartxerox.pipeline.save_user_email',
)


# ======================
# PASSWORD VALIDATION
# ======================

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

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ======================
# INTERNATIONAL
# ======================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ======================
# STATIC FILES
# ======================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# ======================
# MEDIA FILES
# ======================

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# ======================
# DEFAULT FIELD
# ======================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ======================
# FILE LIMITS
# ======================

DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800
DATA_UPLOAD_MAX_NUMBER_FIELDS = None


# ======================
# RAZORPAY
# ======================

RAZORPAY_KEY_ID = "rzp_test_RmdIpA3ijpGtom"
RAZORPAY_KEY_SECRET = "***********************"


# ======================
# EMAIL CONFIG
# ======================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'smartxeroxservice26@gmail.com'
EMAIL_HOST_PASSWORD = 'tllpuaylasqrdyws'

# SECURITY (VERY IMPORTANT FOR RENDER)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')