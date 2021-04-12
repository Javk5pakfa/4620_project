import sys
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta
import tkinter


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
                       fname=None, lname=None, hire_date=None):
        """
        This method queries the database about specific employees based on
        information provided.

        Precondition: number of options provided > 0
        emp_id is int, hire_date is date, others are strings.

        :param emp_id: Employee ID. Default none.
        :param region: Region name. Default none.
        :param fname: First name. Default none.
        :param lname: Last name. Default none.
        :param hire_date: Hire date. Default none.
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
                if region is None:
                    query = query + "Emp_Fname={} ".format(fname)
                else:
                    query = query + "and Emp_Fname={} ".format(fname)
            if lname is not None:
                if region is None and fname is None:
                    query = query + "Emp_Lname={} ".format(lname)
                else:
                    query = query + "and Emp_Lname={} ".format(lname)
            if hire_date is not None:
                if region is None and fname is None and lname is None:
                    query = query + "Emp_Hiredate={} ".format(hire_date)
                else:
                    query = query + "and Emp_Hiredate={} ".format(hire_date)

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

    def query_project(self, pj_id=None, cus_id=None, emp_id=None,
                      pj_date=None, pj_info=None,
                      pj_eststartdate=None, pj_estenddate=None,
                      pj_estbudget=None, pj_actstartdate=None,
                      pj_actenddate=None, pj_actcost=None):
        """
        This method queries the project table of the database based on given
        information.

        Precondition: Needs to have at least one argument.

        :param pj_id: Project ID.
        :param cus_id: Customer ID.
        :param emp_id: Employee ID of the manager.
        :param pj_date: Project contract date.
        :param pj_info: Project description.
        :param pj_eststartdate: Project estimated start date.
        :param pj_estenddate: Project estimated end date.
        :param pj_estbudget: Project estimated budget.
        :param pj_actstartdate: Actual start date.
        :param pj_actenddate: Actual end date.
        :param pj_actcost: Actual cost of the project.
        :return: A list of tuples containing project information.
        """

        query = "select * from project where "
        row_names = ["Proj_ID", "Cus_ID", "Emp_ID", "Proj_Date",
                     "Proj_Descrpt", "Proj_EstDateSt", "Proj_EstDateEnd",
                     "Proj_EstBudget", "Proj_ActDateSt",
                     "Proj_ActDateEnd", "Proj_ActCost"]

        options = (pj_id, cus_id, emp_id, pj_date, pj_info,
                   pj_eststartdate, pj_estenddate, pj_estenddate,
                   pj_estbudget, pj_actstartdate, pj_actenddate, pj_actcost)
        options_index = []
        arguments = ()

        index = 0
        for item in options:
            if item is not None:
                arguments.__add__(item)
                options_index.append(index)
            index += 1

        count = 0
        for arg in arguments:
            if count == 0:
                query = query + "{}={} ".format(
                    row_names[options_index[count]],
                    arg)
            else:
                query = query + "and {}={} ".format(
                    row_names[options_index[count]],
                    arg)
            count += 1

        try:
            self.dbCursor.execute(query)
            return self.dbCursor.fetchall()
        except mysql.connector.Error as err:
            print(err)

    def query_project_schedule(self):
        pass

    def query_assignment(self):
        pass

    def query_worklog(self):
        pass
