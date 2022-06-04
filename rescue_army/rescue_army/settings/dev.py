from .common import *

from dotenv import load_dotenv

load_dotenv()

DEBUG = True


ALLOWED_HOSTS = ["*"]
import mimetypes

mimetypes.add_type("application/javascript", ".js", True)

import dj_database_url

DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
    # {
    # "ENGINE": "django.db.backends.postgresql",
    # "NAME": os.getenv("DB_NAME"),
    # "USER": os.getenv("DB_USER"),
    # "PASSWORD": os.getenv("DB_PASSWORD"),
    # "HOST": os.getenv("DB_HOST"),
    # "PORT": os.getenv("DB_PORT"),
    # }
}

SECRET_KEY = os.getenv("SECRET_KEY")
