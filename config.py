import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = "student_management"
APP_SECRET_KEY = os.getenv("SECRET_KEY")
MYSQL_PORT = os.getenv("MYSQL_PORT")