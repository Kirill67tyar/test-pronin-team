import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("MAILHOG_HOST", "localhost")
EMAIL_PORT = int(os.getenv("MAILHOG_PORT", 1025))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "test-pronin-team@yandex.ru")
