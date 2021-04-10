import sys
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta
import tkinter
import tkinter.ttk
import tkinter.messagebox


class Database:
    def __init__(self):
        try:
            self.dbConnection = mysql.connector.connect(
                host="jack-test-db.cq0gc7w0rwke.us-east-1.rds.amazonaws.com",
                user="Javk5pakfa",
                password="GoJack123CU!",
                database="4620Test")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.dbCursor = self.dbConnection.cursor()

    def __del__(self):
        self.dbCursor.close()
        self.dbConnection.close()

    def query_generic_table(self, table_name):
        query = "select * from {}"

        self.dbCursor.execute(query, table_name)
        result = self.dbCursor.fetchall()
        return result

    def query_employee(self):
        pass

    def query_project(self):
        pass

    def query_project_schedule(self):
        pass

    def query_assignment(self):
        pass

    def query_worklog(self):
        pass
