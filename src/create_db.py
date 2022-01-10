import mysql.connector

from __init__ import create_app
from utils.configs import SQL_HOST, SQL_PASSWORD, SQL_USERNAME

mydb = mysql.connector.connect(
    host=SQL_HOST,
    user=SQL_USERNAME,
    passwd=SQL_PASSWORD,
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")

mycursor.execute("SHOW DATABASES")

for db in mycursor:
    print(db)
