import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key
from split_settings.tools import include


load_dotenv()

include(
    "components/apps.py",
    "components/middleware.py",
    "components/templates.py",
    "components/database.py",
    "components/cache.py",
    "components/celery_cfg.py",
    "components/smtp_cfg.py",
)

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

DEBUG = os.getenv("DJANGO_DEBUG", False) == "True"

ALLOWED_HOSTS = []


ROOT_URLCONF = 'core.urls'


WSGI_APPLICATION = 'core.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    "127.0.0.1",
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_PERMISSION_CLASSES': [
        'api.v1.permissions.IsAuthenticatedAndAuthorOrReadOnly',
    ]
}

COLLECT_LIST = "collections:{page}:list"
COLLECT_DETAIL = "collections:{collect_id}:detail"
PAYMENT_LIST = "collections:{collect_id}:payments:{page}:list"
PAYMENT_DETAIL = "collections:{collect_id}:payments:{payment_id}:detail"
CACHE_TTL = 60 * 5
