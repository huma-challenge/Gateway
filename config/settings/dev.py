from config.settings.base import *

import environ
import os

# Define and loads env var files
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR / "config/django.dev.env"))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

# Create A list of hosts from env var
ALLOWED_HOSTS = str(env("ALLOWED_HOSTS")).strip('"').strip().split()


INSTALLED_APPS += [
    "gateway.account_manager",
]
ROOT_URLCONF = "config.urls.dev"
