#config.py
from dotenv import load_dotenv
import os
load_dotenv()
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{os.getenv('MY_SQL_PASSWORD')}@mysqldb/pokemon_user_db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "your_secret_key"