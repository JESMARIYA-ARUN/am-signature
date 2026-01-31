"""
Django settings for am_signature project.

This file contains all project-level configuration such as
database, static files, authentication redirects, and email setup.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# SECURITY & DEBUG
# ==================================================

# Secret key is loaded from environment variables for safety
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# Debug should be True only in development
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",") if os.environ.get("ALLOWED_HOSTS") else ["localhost", "127.0.0.1"]
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS if h.strip()]



# ==================================================
# APPLICATIONS
# ==================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'accounts',
    'products',
    'orders',
]


# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ==================================================
# URL & TEMPLATE CONFIGURATION
# ==================================================

ROOT_URLCONF = 'am_signature.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Global templates folder
        'DIRS': [BASE_DIR / 'templates'],

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

WSGI_APPLICATION = 'am_signature.wsgi.application'


# ==================================================
# DATABASE CONFIGURATION (PostgreSQL)
# ==================================================

# DATABASES = {
#     "default": {
#         "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
#         "NAME": os.environ.get("DB_NAME", "am_signature_db"),
#         "USER": os.environ.get("DB_USER", "postgres"),
#         "PASSWORD": os.environ.get("DB_PASSWORD", ""),
#         "HOST": os.environ.get("DB_HOST", "localhost"),
#         "PORT": os.environ.get("DB_PORT", "5432"),
#     }
# }
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}



# ==================================================
# MEDIA FILES (User uploads)
# ==================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ==================================================
# PASSWORD VALIDATION
# ==================================================

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


# ==================================================
# INTERNATIONALIZATION
# ==================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==================================================
# STATIC FILES (CSS, JS, Images)
# ==================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]



# ==================================================
# EMAIL CONFIGURATION (BREVO SMTP)
# ==================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp-relay.brevo.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")

# Default sender email
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    "A&M <no-reply@example.com>"
)

# Emails that receive admin order notifications
ADMIN_NOTIFICATION_EMAILS = (
    os.environ.get("ADMIN_NOTIFICATION_EMAILS", "").split(",")
    if os.environ.get("ADMIN_NOTIFICATION_EMAILS")
    else []
)


# ==================================================
# AUTHENTICATION REDIRECTS
# ==================================================

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "products:product_list"
LOGOUT_REDIRECT_URL = "login"


# ==================================================
# DEFAULT PRIMARY KEY
# ==================================================


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if os.environ.get("CSRF_TRUSTED_ORIGINS") else []

