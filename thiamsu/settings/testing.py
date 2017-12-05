from thiamsu.settings.base import *
import dj_database_url

'''
Settings for testing environment deployed on Heroku
'''

ALLOWED_HOSTS = ['thiamsu-testing.herokuapp.com']

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
