import dj_database_url

from thiamsu.settings.base import *

"""
Settings for staging environment deployed on Heroku
"""

ALLOWED_HOSTS = ["*"]

# WhiteNoise
MIDDLEWARE.extend(["whitenoise.middleware.WhiteNoiseMiddleware"])
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
