import os
from dotenv import load_dotenv

ENV = os.getenv("APP_ENV", "development")
env_file = f".env.{ENV}"

load_dotenv(env_file)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

print(f"Running in {ENV} environment")
