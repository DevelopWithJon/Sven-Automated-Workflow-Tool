"""Project configurations."""
import os
import re
from dotenv import load_dotenv  # type: ignore

load_dotenv()

EMAILUSERNAME = os.getenv("EMAILUSERNAME")
EMAILPASSWORD = os.getenv("EMAILPASSWORD")
EPA_API = os.getenv("EPA_API")
GEOLOCATE_API = os.getenv("GEOLOCATE_API")
DATABASE_URL = os.getenv("CLEARDB_DATABASE_URL")
DB_NAME = os.getenv("DB_NAME", "")
MAPS_API = os.getenv("MAPS_API")
SQLALCHEMY_DATABASE_URI = DATABASE_URL + "/" + DB_NAME
SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_TRACK_MODIFICATIONS = False
if SQLALCHEMY_DATABASE_URI:
    SQL_USERNAME = re.findall(r'(?<=://)[a-zA-Z0-9]+(?=:)', SQLALCHEMY_DATABASE_URI)[0]
    SQL_PASSWORD = re.findall(fr'(?<={SQL_USERNAME}:)[a-zA-Z0-9]+(?=@)', SQLALCHEMY_DATABASE_URI)[0]
    SQL_HOST = re.findall(r'(?<=@).*(?=/)',SQLALCHEMY_DATABASE_URI)[0]
    
else:
    SQL_USERNAME = "root"
    SQL_PASSWORD = "Svenpassword"
    SQL_HOST = "localhost"
