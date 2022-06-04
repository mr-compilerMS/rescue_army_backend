from .common import *


DEBUG = False

ALLOWED_HOSTS = ["rescue-army.herokuapp.com"]

import dj_database_url

DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": os.getenv("DB_NAME"),
    #     "USER": os.getenv("DB_USER"),
    #     "PASSWORD": os.getenv("DB_PASSWORD"),
    #     "HOST": os.getenv("DB_HOST"),
    #     "PORT": os.getenv("DB_PORT"),
    # }
}

SECRET_KEY = os.getenv("SECRET_KEY")
