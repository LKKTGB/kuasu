from thiamsu.settings.base import *

# WhiteNoise
MIDDLEWARE.extend([
    'whitenoise.middleware.WhiteNoiseMiddleware',
])
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
