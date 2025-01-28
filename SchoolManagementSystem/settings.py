from pathlib import Path
import os

from django.contrib.admin import AdminSite

# Define custom admin titles directly through settings.py
ADMIN_SITE_HEADER = 'KIHS - MANAGEMENT SYSTEM'  # Set a custom header title
ADMIN_SITE_TITLE = 'KIHS - MANAGEMENT SYSTEM'  # Set a custom page title
ADMIN_INDEX_TITLE = 'Welcome to KIHS - SMS'  # Custom index page title

# Customize admin interface directly by importing and applying this to AdminSite
AdminSite.site_header = ADMIN_SITE_HEADER
AdminSite.site_title = ADMIN_SITE_TITLE
AdminSite.index_title = ADMIN_INDEX_TITLE

JET_DEFAULT_THEME = 'default'  # Reset to the default theme
JET_SIDE_MENU_COMPACT = True  # Optional: Enables a compact side menu
JET_CHANGE_FORM_SIBLING_LINKS = True  # Optional: Disable sibling links in change forms

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-&jeahvet&1#bs*d)ce+m*^!0jh$*ch4gz0)@7%ga(2f#mg^y=m'

DEBUG = True

ALLOWED_HOSTS = ['192.168.1.191', '127.0.0.1', 'localhost:8000', 'https://sgwsm2vt-8000.euw.devtunnels.ms']

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admissions',
    'academics',
    'bursary',
    'staff',
    'import_export',
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

ROOT_URLCONF = 'SchoolManagementSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'SchoolManagementSystem.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,  # Increase the timeout to 20 seconds
        },
    },
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "backend"  # Main Django App Folder Name

STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    str(APPS_DIR / "static"),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Media settings for file uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JET_PROJECT = 'Your Custom Title'
JET_PROJECT_TAGLINE = 'Your Tagline or Description'