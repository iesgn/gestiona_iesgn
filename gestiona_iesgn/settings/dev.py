from .base import *

SECRET_KEY = "dev-insecure-key-only-for-local-development"

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True
ALLOWED_HOSTS = ["*"]

SITE_URL = "http://localhost:8000"
SITE_URL_STATIC = "http://localhost:8000/static/"
REDMINE_URL = "https://dit.gonzalonazareno.org/redmine/"

STATIC_ROOT = BASE_DIR / "staticfiles"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
