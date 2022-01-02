import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Svenpassword",
)

mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE mydatabase")

mycursor.execute("SHOW DATABASES")

for db in mycursor:
    print(db)
    
