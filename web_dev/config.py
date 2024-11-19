# config.py
from dotenv import load_dotenv
import os
load_dotenv()
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:{os.getenv('MY_SQL_PASSWORD')}@172.17.0.3/pokemon_user_db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY= "your_secret_key"

