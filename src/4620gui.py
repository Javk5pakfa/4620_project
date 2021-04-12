import sys
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta
import tkinter
import tkinter.ttk
import tkinter.messagebox


class Database:
    """
    This class is the model object that handles actual database data.
    """

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
        """
        This method takes in a table_name and returns the table data
        found by the cursor in the database.

        :param table_name: The table name to be queried.
        :return: a list of tuples from table_name.
        """

        query = "select * from {}"
        try:
            self.dbCursor.execute(query, table_name)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_NO_SUCH_TABLE:
                print("Table doesn't exist.")
            else:
                print(err)

        result = self.dbCursor.fetchall()
        return result

    def query_employee(self,
                       emp_id=None, region=None,
                       fname=None, lname=None):
        """
        This method queries the database about specific employees based on
        information provided.

        :precondition number of options provided > 0
        emp_id is int, hire_date is date, others are strings.

        :param emp_id: Employee ID. Default none.
        :param region: Region name. Default none.
        :param fname: First name. Default none.
        :param lname: Last name. Default none.
        :return: a list of tuples containing target employee(s).
        """

        results = None

        if emp_id is not None:
            try:
                self.dbCursor.execute("select * from employee where Emp_ID={}",
                                      emp_id)
                results = self.dbCursor.fetchall()
            except mysql.connector.Error as err:
                print(err)
        else:
            query = "select * from employee where "
            if region is not None:
                query = query + "region.Region_ID=employee.Region_ID " \
                                "and Region_Name={} ".format(region)
            if fname is not None:
                query = query + "and Emp_Fname={}".format(fname)
            if lname is not None:
                query = query + "and Emp_Lname={}".format(lname)

            try:
                self.dbCursor.execute(query)
                results = self.dbCursor.fetchall()
            except mysql.connector.Error as err:
                print(err)

        if results is None:
            print("Error while querying table.")
            quit()
        else:
            return results

    def query_project(self):
        pass

    def query_project_schedule(self):
        pass

    def query_assignment(self):
        pass

    def query_worklog(self):
        pass
