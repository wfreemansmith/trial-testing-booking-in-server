import os
import sys
import argparse
from dotenv import load_dotenv

ENV = os.getenv("APP_ENV", "development")
env_file = f".env.{ENV}"

load_dotenv(env_file)

SQL_DB = os.getenv("SQL_DB")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
LEGACY_DB_HOST = os.getenv("LEGACY_DB_HOST")
LEGACY_DB_NAME = os.getenv("LEGACY_DB_NAME")
USERDOMAIN = os.getenv("USERDOMAIN")
USERNAME = os.getenv("USERNAME")
## also include DRIVER for SQL Server

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