import os
import mimetypes
from pathlib import Path
from decouple import config


config.encoding = 'cp1251'

# CSS and JS MIME types
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("application/javascript", ".js", True)


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)


try:
    from staff_configurations import staff_settings as _staff_set
    # If you exported a dict only:
    #DATABASES = _core_conf.DATABASES
    # If you also made apply(), you could do:
    _staff_set.apply(globals())
except Exception as e:
    # Fail loud or soft — your call:
    raise RuntimeError(f"Failed to load staff DB overrides: {e}")


ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.sites',  # Required for allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'easyaudit',
    'daphne',
    'channels',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'foundations',
    'accounts',
    'customers',
    'orders',
    'crispy_forms',
    'versatileimagefield',
    'notifications',



]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WHITENOISE STATIC
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'tailoring_management_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tailoring_management_system.wsgi.application'
ASGI_APPLICATION = "tailoring_management_system.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

NOTIFICATIONS_PAGE_SIZE = 20

CSRF_TRUSTED_ORIGINS = [
]


AUTH_USER_MODEL = 'accounts.User'


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


SITE_ID = 1

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = 'accounts:home_page'  # Change as necessary
LOGOUT_URL = 'accounts:logout'  # Change as necessary
LOGIN_REDIRECT_URL = 'accounts:home_page'  # Redirect URL after login
LOGOUT_REDIRECT_URL = 'accounts:account_login'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Authentication is done using email only
ACCOUNT_EMAIL_REQUIRED = True  # Email is required for signup
ACCOUNT_USERNAME_REQUIRED = False  # No username is needed
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'  # No username field in the User model
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Optional: requires email verification
ACCOUNT_UNIQUE_EMAIL = True  # Ensure email is unique

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
ACCOUNT_CONFIRM_EMAIL_ON_GET = True


ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',
    'login': 'accounts.forms.CustomLoginForm',
}

ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'accounts:account_login'


# CELERY SETTINGS
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_ENABLE_UTC = False
if DEBUG:
    CELERY_BROKER_URL = config('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
else:
    CELERY_BROKER_URL = config('LIVE_CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = config('LIVE_CELERY_RESULT_BACKEND')


if DEBUG:
    pass
else:
    # pass
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31449600
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'add_ip': {
            '()': 'foundations.custom_handler.AddIPFilter',
        },
    },
    'handlers': {
        # Existing handlers
        'error_logfile': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'error_formatter',
        },
        'access_logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'access.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'access_formatter',
            'filters': ['add_ip'],  # Attach the filter
        },
        # New handler for sending error emails
        'mail_admins': {
            'level': 'ERROR',
            'class': 'foundations.custom_handler.CustomAdminEmailHandlerBasic',
            'include_html': True,  # Optionally include HTML content in emails
        },
    },
    'formatters': {
        # Existing formatters
        'error_formatter': {
            'format': '{levelname:8s} {asctime:s} {name:12s} {threadName} {thread:d} {module} {filename:4s} {lineno:d} {name} {funcName:4s} {process:d} {message} {exc_info}',
            'style': '{',
        },
        'access_formatter': {
            'format': '{levelname:8s} {asctime:s} {ip} {name:12s} {module} {filename:4s} {lineno:d} {funcName:4s} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error_logfile', 'access_logfile', 'mail_admins'],  # Include 'mail_admins' handler
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# EASY AUDIT SETUP
DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = True
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = True
DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA = [
    # 'tenant_administrations.Domain',
]
DJANGO_EASY_AUDIT_UNREGISTERED_URLS_EXTRA = [
    'api/v1/base/'
]