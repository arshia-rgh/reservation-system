from .base import *

# Set DEBUG to False in production environment
DEBUG = False

# ALLOWED_HOSTS is a list of strings representing the host/domain names that this Django site can serve.
# It's fetched from the environment variable ALLOWED_HOSTS and split by space.
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")

# DATABASES is a dictionary containing the settings for all databases to be used in the project.
# Here, we have a single database named 'default' using PostgreSQL.
# The database connection details are fetched from environment variables.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # The database backend to use.
        "NAME": os.environ.get("DB_NAME"),  # The name of the database.
        "USER": os.environ.get("DB_USER"),  # The username to connect to the database.
        "PASSWORD": os.environ.get("DB_PASSWORD"),  # The password to connect to the database.
        "HOST": os.environ.get("DB_HOST"),  # The host of the database.
        "PORT": os.environ.get("DB_PORT"),  # The port of the database.
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"
