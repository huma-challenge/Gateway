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
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "gateway.account_manager",
]

ROOT_URLCONF = "config.urls.dev"

REST_FRAMEWORK = {
    # YOUR SETTINGS
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Gateway of MicroServices",
    "DESCRIPTION": "A gateway for micro-services",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

STATIC_ROOT = BASE_DIR / "statics"
