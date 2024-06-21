import os.path

from config.components.boilerplate import BASE_DIR

STATIC_DIR = BASE_DIR

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(STATIC_DIR.parent, "static/")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
