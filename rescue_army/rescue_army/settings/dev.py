from .common import *

from dotenv import load_dotenv

load_dotenv()

DEBUG = True


ALLOWED_HOSTS = ["*"]
import mimetypes

mimetypes.add_type("application/javascript", ".js", True)

import dj_database_url

DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}

SECRET_KEY = os.getenv("SECRET_KEY")
