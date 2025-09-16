import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DJANGO_DEBUG", False) == "True"


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "fees.apps.FeesConfig",
    "users.apps.UsersConfig",
    "api.apps.ApiConfig",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
