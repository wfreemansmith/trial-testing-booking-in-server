import os
import sys
import argparse
from dotenv import load_dotenv

if 'pytest' in sys.modules:
    ENV = "testing"
else:
    ENV = os.getenv("APP_ENV", "development")

env_file = f".env.{ENV}"
print(env_file)

load_dotenv(env_file)

# Database
SQL_DB = os.getenv("SQL_DB")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("DB_PORT")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
LEGACY_DB_HOST = os.getenv("LEGACY_DB_HOST")
LEGACY_DB_NAME = os.getenv("LEGACY_DB_NAME")
USERDOMAIN = os.getenv("USERDOMAIN")
USERNAME = os.getenv("USERNAME")

# Files.com
FILE_UPLOAD_API_KEY = os.getenv("FILE_UPLOAD_API_KEY")
FILE_UPLOAD_BASE_URL = os.getenv("FILE_UPLOAD_BASE_URL")

# debug mode
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', dest='debug')
args = parser.parse_args()

DEBUG = args.debug

# test mode
IS_TEST = 'pytest' in sys.modules

print(f"Running in {ENV} environment")

if DEBUG:
    print("Debug mode on")
if IS_TEST:
    print("Testing with Pytest")