import os
from datetime import datetime

from config.components.boilerplate import BASE_DIR

LOGGING_DIR = os.path.join(BASE_DIR.parent, "logs")

if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(
                LOGGING_DIR, "{:%Y-%m-%d}.log".format(datetime.now())
            ),
            "when": "midnight",
            "backupCount": 7,
            "encoding": "utf-8",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "ERROR",
    },
}
