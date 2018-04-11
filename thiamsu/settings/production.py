from thiamsu.settings.base import *
import dj_database_url

'''
Settings for production environment deployed on Heroku
'''
DEBUG = False

GA_TRACKING_ID = 'UA-114678735-2'

ALLOWED_HOSTS = [
    'kuasu.tgb.org.tw'
]

# WhiteNoise
MIDDLEWARE.extend([
    'whitenoise.middleware.WhiteNoiseMiddleware',
])
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
