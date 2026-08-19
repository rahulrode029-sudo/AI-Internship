import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv(
    "APP_NAME",
    "AI Document Research Assistant"
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0"
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)