"""
WSGI config for thiamsu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

try:
    import dotenv
    dotenv.read_dotenv()
except ImportError:
    pass
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings.development')

application = get_wsgi_application()
