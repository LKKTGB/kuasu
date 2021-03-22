import os

from thiamsu.settings.production import *

DEBUG = True if "DEBUG" in os.environ else False
ALLOWED_HOSTS = ["kuasu-stage.azurewebsites.net"]
