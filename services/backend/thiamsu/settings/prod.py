import os

import dj_database_url

from thiamsu.settings.base import *

"""
Settings for production environment deployed on Heroku
"""
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = False

# security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

GA_TRACKING_ID = "G-HKJK1VPKGG"

ALLOWED_HOSTS = ["kuasu.tgb.org.tw", "kuasu-production.azurewebsites.net"]

# WhiteNoise
MIDDLEWARE.extend(["whitenoise.middleware.WhiteNoiseMiddleware"])
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "ERROR"),
        }
    },
}
