from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers", "cookies", "json", "query_string"]