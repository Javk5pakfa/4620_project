# import sys
import mysql.connector
from mysql.connector import errorcode
# from datetime import date, datetime, timedelta
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
                ErrorMessageWindow(err)
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
                ErrorMessageWindow(err)

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
                ErrorMessageWindow(err)
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
                ErrorMessageWindow(err)

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
            ErrorMessageWindow(err)

    def query_project_tasks(self, project_data):
        """
        This method delivers the assignments associated with a particular
        project.

        Precondition: project_data contains one project information only.

        :param project_data: A list of tuples containing the project
        information.
        :return: A list of tuples of assignment information.
        """

        # Get project ID.
        project_id = project_data[0][0]
        query = "select task_datest, task_dateend, task_info, skill_descrpt, " \
                "TS_Qty " \
                "from skill, task_skills, task " \
                "where task_skills.task_id = task.task_id " \
                "and proj_id = {} " \
                "and task_skills.skill_id = skill.skill_id " \
                "order by task_datest".format(project_id)

        try:
            self.dbCursor.execute(query)
            return self.dbCursor.fetchall()
        except mysql.connector.Error as err:
            ErrorMessageWindow(err)

    def query_assignment(self, project_data):
        """
        This method produces data for the assignment window.

        :param project_data: Data of project of interest.
        :return: Assignment data in a list of tuples.
        """

        project_id = project_data[0][0]
        query = "select task_datest, task_dateend, task_info, " \
                "skill_descrpt, asn_id, emp_lname, emp_fname, " \
                "asn_dateest, asn_dateend " \
                "from assign, employee, task, skill, task_skills " \
                "where task_skills.task_id = task.task_id " \
                "and proj_id = {} " \
                "and task_skills.skill_id = skill.skill_id " \
                "and assign.emp_id = employee.emp_id " \
                "and assign.ts_id = task_skills.ts_id " \
                "GROUP BY asn_id " \
                "ORDER BY task_datest".format(project_id)

        try:
            self.dbCursor.execute(query)
            return self.dbCursor.fetchall()
        except mysql.connector.Error as err:
            ErrorMessageWindow(err)

    def query_employee_skill(self):
        """
        This method queries the database of the employee/skill inventory.

        :return: A list of tuples showing skill, first name, and last name
        of the employee that has that skill.
        """

        query = "select Skill_Descrpt, Emp_Fname, Emp_Lname from " \
                "skill, employee, empskill " \
                "where employee.Emp_ID = empskill.Emp_ID " \
                "and skill.Skill_ID = empskill.Skill_ID "

        try:
            self.dbCursor.execute(query)
            return self.dbCursor.fetchall()
        except mysql.connector.Error as err:
            ErrorMessageWindow(err)

    def query_worklog(self):
        """
        This method returns the work-log table.

        :return: A list of tuples representing work-log table.
        """

        query = "select * from worklog"

        try:
            self.dbCursor.execute(query)
            return self.dbCursor.fetchall()
        except mysql.connector.Error as err:
            ErrorMessageWindow(err)

    def query_customer_cusid(self, cus_id):
        """
        This method returns customer info based on customer id.

        :param cus_id: Customer ID.
        :return: A list of tuples containing customer information.
        """

        query = "select * from customer where cus_id = {}".format(cus_id)

        try:
            self.dbCursor.execute(query)
            return self.dbCursor.fetchall()
        except mysql.connector.Error as err:
            ErrorMessageWindow(err)

    def query_region_id(self, region_id):
        """
        This method returns region table with region id provided.

        :param region_id: Region id to query.
        :return: A list of tuples containing region info.
        """

        query = "select * from region where region_id={}".format(region_id)

        try:
            self.dbCursor.execute(query)
            return self.dbCursor.fetchall()
        except mysql.connector.Error as err:
            ErrorMessageWindow(err)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


class ReportWindow:
    """
    This class represents the report window.
    """

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.wm_title("Database Report Window")

        tkinter.Label(self.window, width=50, text="Report Window").grid(
            pady=20, column=1, row=1
        )

        self.project_schedule_window = ProjectScheduleWindow
        self.employee_skill_window = EmpSkillWindow

        tkinter.Button(
            self.window, width=25, text="Employee-Skill Inventory",
            command=self.employee_skill_window
        ).grid(
            pady=10, column=1, row=2
        )
        tkinter.Button(
            self.window, width=25, text="Project Schedule",
            command=self.project_schedule_window
        ).grid(
            pady=10, column=1, row=3
        )
        tkinter.Button(
            self.window, width=25, text="Assignment Form"
        ).grid(
            pady=10, column=1, row=4
        )
        tkinter.Button(
            self.window, width=25, text="Work-log"
        ).grid(
            pady=10, column=1, row=5
        )

        self.window.mainloop()


class EmpSkillWindow:
    def __init__(self):
        # Variable declaration.
        test_database = Database()
        test_data = test_database.query_employee_skill()

        # Window definition.
        self.window = tkinter.Tk()
        self.window.wm_title("Employee-Skill Inventory")
        tkinter.Label(self.window, text="Table View", width=50).grid(
            pady=5, column=1, row=1
        )

        # Table definition.
        self.employee_skill_view = tkinter.ttk.Treeview(self.window)
        self.employee_skill_view.grid(pady=5, column=1, row=2)
        self.employee_skill_view["show"] = "headings"
        self.employee_skill_view["columns"] = ("Skill", "lname",
                                               "fname")

        self.employee_skill_view.heading("Skill", text="Skill")
        self.employee_skill_view.heading("lname", text="Last Name")
        self.employee_skill_view.heading("fname", text="First Name")

        self.employee_skill_view.column("Skill", width=150)
        self.employee_skill_view.column("lname", width=120)
        self.employee_skill_view.column("fname", width=120)

        # Load data into window.
        for item in test_data:
            self.employee_skill_view.insert('', 'end', values=item)


# -----------------------------------------------------------------------------

class ProjectScheduleWindow:
    """
    This class represents the window where options for different types of
    project reports are displayed.
    """

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.wm_title("Project Selection Window")

        tkinter.Label(self.window, width=50,
                      text="Project Selection Window").grid(
            pady=20, column=1, row=1
        )

        self.window.mainloop()


class UpdateWindow:

    def __init__(self):
        self.window = tkinter.Tk()
        self.window.wm_title("Database Update Window")

        self.window.mainloop()


class SearchWindow:
    pass


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


class ErrorMessageWindow:
    """
    This class represents a generic error message window that pops whenever
    a user input results in error.
    """

    def __init__(self, message):
        self.window = tkinter.Tk()
        self.window.wm_title("ERROR")

        self.error_message = message
        tkinter.Label(self.window, text=self.error_message).pack(
            pady=10, padx=10
        )

        tkinter.Button(
            self.window, text="Quit", command=self.window.destroy
        ).pack()


class HomePage:
    """
    This class represents the home screen of the database GUI. WIP.
    """

    def __init__(self):
        self.homePageWindow = tkinter.Tk()
        self.homePageWindow.wm_title("4620 Project Database Access Terminal")
        # self.database = Database()

        # Width of home screen.
        tkinter.Label(self.homePageWindow, width=50, text="Home Page").grid(
            pady=20, column=1, row=1
        )

        self.update_window = UpdateWindow
        self.report_window = ReportWindow

        # Buttons.
        tkinter.Button(
            self.homePageWindow, width=25, text="Report",
            command=self.report_window
        ).grid(
            pady=10, column=1, row=2
        )
        tkinter.Button(
            self.homePageWindow, width=25, text="Search"
        ).grid(
            pady=10, column=1, row=3
        )
        tkinter.Button(
            self.homePageWindow, width=25, text="Update",
            command=self.update_window
        ).grid(
            pady=10, column=1, row=4
        )
        tkinter.Button(
            self.homePageWindow, width=25, text="Quit",
            command=self.homePageWindow.destroy
        ).grid(
            pady=10, column=1, row=5
        )

        self.homePageWindow.mainloop()


mainPage = HomePage()
# mainPage.database.dbCursor.close()
# mainPage.database.dbConnection.close()
