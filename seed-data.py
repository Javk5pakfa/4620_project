#!usr/local/bin

import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='jack-test-db.cq0gc7w0rwke.us-east-1.rds.amazonaws.com',
                                         database='ConstructCo',
                                         user='Javk5pakfa',
                                         password='GoJack123CU!')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        # Assignment goes here.

        cursor.close()
        connection.close()
        print("MySQL connection is closed")