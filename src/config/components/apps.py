import os
import sys

from config.components.boilerplate import BASE_DIR

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY = [
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "cachalot",
    "django_extensions",
]

sys.path.insert(0, os.path.join(BASE_DIR, "apps"))


LOCAL_APPS = ["accounts", "restaurants", "votes"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY + LOCAL_APPS
