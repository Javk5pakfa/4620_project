#!usr/local/bin

import mysql.connector
from mysql.connector import Error

db_name = "4620Project"

try:
    connection = mysql.connector.connect(host='jack-test-db.cq0gc7w0rwke.us-east-1.rds.amazonaws.com',
                                        user='Javk5pakfa',
                                        password='GoJack123CU!')
    if connection.is_connected():
        print("1st connection successful.")
        cursor = connection.cursor()
        print("create database " + db_name)
        cursor.execute("create database " + db_name)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("1st connection is closed")

try:
    connection = mysql.connector.connect(host='jack-test-db.cq0gc7w0rwke.us-east-1.rds.amazonaws.com',
                                        database=db_name,
                                        user='Javk5pakfa',
                                        password='GoJack123CU!')
    if connection.is_connected():
        print("2nd connection successful.")
        cursor = connection.cursor()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("2nd connection is closed")
