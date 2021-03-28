#!usr/local/bin

import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='jack-test-db.cq0gc7w0rwke.us-east-1.rds.amazonaws.com',
                                        user='Javk5pakfa',
                                        password='GoJack123CU!')
    if connection.is_connected():
        print("1st connection successful.")
        cursor = connection.cursor()
        print("create database 4620project")
        cursor.execute("create database 4620project")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("1st connection is closed")

# try:
#     connection = mysql.connector.connect(host='jack-test-db.cq0gc7w0rwke.us-east-1.rds.amazonaws.com',
                                        
#                                         user='Javk5pakfa',
#                                         password='GoJack123CU!')
#     if connection.is_connected():
#         print("1st connection successful.")
#         cursor = connection.cursor()
#         print("create database 4620project")
#         cursor.execute("create database 4620project")

# except Error as e:
#     print("Error while connecting to MySQL", e)
# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
#         print("1st connection is closed")