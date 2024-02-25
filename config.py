from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")