from .common import *


DEBUG = False

ALLOWED_HOSTS = ["rescue-army.herokuapp.com"]

import dj_database_url

DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}

SECRET_KEY = os.getenv("SECRET_KEY")

DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

GS_BUCKET_NAME = "rescue-army.appspot.com"

from google.oauth2 import service_account

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    BASE_DIR / "rescue-army-firebase-adminsdk-rhxbz-14150ec586.json"
)
