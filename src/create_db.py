import mysql.connector

from __init__ import create_app

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Svenpassword",
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")

mycursor.execute("SHOW DATABASES")

for db in mycursor:
    print(db)
