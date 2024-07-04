import os

from dotenv import load_dotenv

from .base import BASE_DIR

# Load environment variables from .env file
# Returns: True if .env file is loaded successfully, False otherwise
is_set = load_dotenv(os.path.join(BASE_DIR, ".env"))

# Get the MODE environment variable
# Returns: The value of MODE environment variable if set, None otherwise
MODE = os.environ.get("MODE")

if is_set:
    # Print a message indicating that environment variables are loaded from .env file
    print("Environment variables loaded from.env file")
    # Print the value of MODE environment variable
    print(f"MODE: {MODE}")

# Depending on the MODE, import the corresponding configuration settings
if MODE == "development":
    from .development import *
elif MODE == "production":
    from .production import *
else:
    # If MODE is neither 'development' nor 'production', raise an exception
    # Raises: Exception with a descriptive error message
    raise Exception(
        "MODE environment variable must be set to either 'development' or 'production'"
    )
