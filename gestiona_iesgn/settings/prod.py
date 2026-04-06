import os
from .base import *

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = False
ALLOWED_HOSTS = ["dit.gonzalonazareno.org"]

SITE_URL = "https://dit.gonzalonazareno.org/gestiona"
SITE_URL_STATIC = "https://dit.gonzalonazareno.org/gestiona/static/"

CSRF_TRUSTED_ORIGINS = [
    "https://dit.gonzalonazareno.org",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "/gestiona/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
