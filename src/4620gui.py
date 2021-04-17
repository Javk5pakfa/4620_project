# import sys
import datetime
import mysql.connector
from mysql.connector import errorcode
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

    def query_employee(self, employee_inputs):
        """
        This method queries the employee table with the given info.

        :param employee_inputs: Collection of inputs about employee.
        :return: A collection of rows from database about said employee.
        """

        query = "select * from employee where "
        row_names = [
            "emp_ID", "Region_ID", "Emp_Lname", "Emp_Mi", "Emp_Fname",
            "Emp_Hiredate"
        ]
        filled_attributes = []

        row_index = 0
        row_options = []
        for item in employee_inputs:
            if item is not None:
                row_options.append(row_index)
                filled_attributes.append(item)
            row_index += 1

        j = 0
        for i in row_options:
            if j == 0:
                query += "{}='{}' ".format(row_names[i], filled_attributes[j])
            else:
                query += "and {}='{}' ".format(row_names[i],
                                               filled_attributes[j])
            j += 1

        try:
            self.dbCursor.execute(query)
            return self.dbCursor.fetchall()
        except mysql.connector.Error as err:
            ErrorMessageWindow(err)

    def query_project(self, project_query_options):
        """
        This method queries the project table of the database based on given
        information.

        Precondition: Needs to have at least one argument.

        :param project_query_options: A list of query entries.
        :return: A list of tuples containing project information.
        """

        query = "select * from project where "
        row_names = ["Proj_ID", "Cus_ID", "Emp_ID", "Proj_Date",
                     "Proj_Descrpt", "Proj_EstDateSt", "Proj_EstDateEnd",
                     "Proj_EstBudget", "Proj_ActDateSt",
                     "Proj_ActDateEnd", "Proj_ActCost"]

        entries = project_query_options
        options_index = []
        arguments = []

        index = 0
        for item in entries:
            if item is not None:
                arguments.append(item)
                options_index.append(index)
            index += 1

        count = 0
        for arg in arguments:
            if count == 0:
                query = query + "{}='{}' ".format(
                    row_names[options_index[count]],
                    arg)
            else:
                query = query + "and {}='{}' ".format(
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
                "and proj_id = '{}' " \
                "and task_skills.skill_id = skill.skill_id " \
                "order by task_datest".format(project_id)

        try:
            self.dbCursor.execute(query)
            return self.dbCursor.fetchall()
        except mysql.connector.Error as err:
            ErrorMessageWindow(err)

    def query_assignment(self, project_id=None, emp_id=None):
        """
        This method produces data for the assignment window.

        :param emp_id: Employee ID of interest
        :param project_id: Project ID of interest.
        :return: Assignment data in a list of tuples.
        """

        query = ""

        if project_id is not None and emp_id is not None:
            query = "select task_datest, task_dateend, task_info, " \
                    "skill_descrpt, asn_id, emp_lname, emp_fname, " \
                    "asn_datest, asn_dateend " \
                    "from assign, employee, task, skill, task_skills " \
                    "where task_skills.task_id = task.task_id " \
                    "and proj_id = '{}' " \
                    "and employee.emp_id = '{}' " \
                    "and task_skills.skill_id = skill.skill_id " \
                    "and assign.emp_id = employee.emp_id " \
                    "and assign.ts_id = task_skills.ts_id " \
                    "ORDER BY task_datest".format(project_id, emp_id)
        elif project_id is None and emp_id is not None:
            query = "select task_datest, task_dateend, task_info, " \
                    "skill_descrpt, asn_id, emp_lname, emp_fname, " \
                    "asn_datest, asn_dateend " \
                    "from assign, employee, task, skill, task_skills " \
                    "where task_skills.task_id = task.task_id " \
                    "and employee.emp_id = '{}' " \
                    "and task_skills.skill_id = skill.skill_id " \
                    "and assign.emp_id = employee.emp_id " \
                    "and assign.ts_id = task_skills.ts_id " \
                    "ORDER BY task_datest".format(emp_id)
        elif project_id is not None and emp_id is None:
            query = "select task_datest, task_dateend, task_info, " \
                    "skill_descrpt, asn_id, emp_lname, emp_fname, " \
                    "asn_datest, asn_dateend " \
                    "from assign, employee, task, skill, task_skills " \
                    "where task_skills.task_id = task.task_id " \
                    "and proj_id = '{}' " \
                    "and task_skills.skill_id = skill.skill_id " \
                    "and assign.emp_id = employee.emp_id " \
                    "and assign.ts_id = task_skills.ts_id " \
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

    # TODO: Expand this method to incorporate employee search.
    def query_worklog(self, emp_id=None):
        """
        This method returns the work-log table.

        :param emp_id: A specific employee to look up for.
        :return: A list of tuples representing work-log table.
        """

        query = "select * from worklog"

        try:
            self.dbCursor.execute(query)
            return self.dbCursor.fetchall()
        except mysql.connector.Error as err:
            ErrorMessageWindow(err)

    # TODO: Probably needs rework/expansion.
    def query_customer(self,
                       cus_id=None,
                       cus_name=None,
                       cus_phone=None):
        """
        This method returns customer info based on customer id.

        :param cus_phone: Phone number of customer.
        :param cus_name: Name of customer.
        :param cus_id: Customer ID.
        :return: A list of tuples containing customer information.
        """

        query = "select * from customer where "

        options = [cus_id, cus_name, cus_phone]
        row_names = ["cus_id", "cus_name", "cus_phone"]
        index = 0
        num_args = 0
        for item in options:
            if index == 0:
                if item is not None:
                    if num_args == 0:
                        query = query + "{}='{}' ".format(row_names[index],
                                                          item)
                    else:
                        query = query + "and {}='{}' ".format(row_names[index],
                                                              item)
                    num_args += 1
            else:
                if item is not None:
                    if num_args == 0:
                        query = query + "{}='{}' ".format(row_names[index],
                                                          item)
                    else:
                        query = query + "and {}='{}' ".format(row_names[index],
                                                              item)
                    num_args += 1
            index += 1

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

        query = "select * from region where region_id='{}'".format(region_id)

        try:
            self.dbCursor.execute(query)
            return self.dbCursor.fetchall()
        except mysql.connector.Error as err:
            ErrorMessageWindow(err)

    def insert_skill(self, skill_info, skill_rate):
        """
        This method inserts one entry into skill table.

        :param skill_info: Information about this skill.
        :param skill_rate: Hour rate of this skill.
        :return: Success message if success || Error if insert error.
        """

        if self.check_input_type(skill_rate, "float"):
            if skill_rate >= 0.0:
                query = "insert into skill(skill_descrpt, skill_rate) " \
                        "values ('{}', '{}')".format(skill_info, skill_rate)

                try:
                    self.dbCursor.execute(query)
                    SuccessMessageWindow("Insert success!")
                except mysql.connector.Error as err:
                    ErrorMessageWindow(err)
                finally:
                    self.dbConnection.commit()
            else:
                ErrorMessageWindow("Skill rate must be non-negative!")
        else:
            ErrorMessageWindow("Skill rate must be a number!")

    def insert_employee(self,
                        region_name,
                        last_name,
                        first_name,
                        hire_date,
                        mi):
        """
        This method inserts a new employee given the information.

        :param region_name: Self-explanatory.
        :param last_name: Self-explanatory.
        :param first_name: Self-explanatory.
        :param hire_date: Self-explanatory.
        :param mi: Middle initials.
        :return: Success message if success || Error if insert error.
        """

        if self.check_input_type(region_name, "Region"):
            if self.check_input_type(hire_date, "Date"):
                if mi != "":
                    query = "insert into employee(Region_ID, " \
                            "Emp_Lname, Emp_Mi, Emp_Fname, Emp_Hiredate) " \
                            "values ((select region_id from region where " \
                            "region_name='{}'), '{}', '{}', '{}', '{}')"
                    query.format(
                        region_name, last_name, mi, first_name, hire_date
                    )

                    try:
                        self.dbCursor.execute(query)
                        SuccessMessageWindow("Insert success!")
                    except mysql.connector.Error as err:
                        ErrorMessageWindow(err)
                    finally:
                        self.dbConnection.commit()
            else:
                ErrorMessageWindow("Date format not valid!")
        else:
            ErrorMessageWindow("Region input not valid!")

    # TODO
    def create_new_project(self):
        pass

    # TODO
    def create_assignments(self):
        pass

    # TODO
    def log_worktime(self):
        pass

    @staticmethod
    def check_input_type(var, type_name):
        """
        This method checks whether if the variable var is the type that
        type_name dictates. True if yes, false otherwise.

        :param var: Value to check.
        :param type_name: Target type.
        :return: True || False.
        """

        type_options = ["int", "float", "Date", "Region"]
        if type_name == type_options[0]:
            return type(var) is int
        elif type_name == type_options[1]:
            return type(var) is float
        elif type_name == type_options[2]:
            return type(var) is datetime.date
        elif type_name == type_options[3]:
            valid_regions = ["NW", "SW", "MN", "MS", "NE", "SE"]
            is_valid = False
            for region in valid_regions:
                if var == region:
                    is_valid = True
            return is_valid
        else:
            Exception("This type doesn't exist in the checker!")


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

        self.employee_skill_window = EmpSkillWindow
        self.project_schedule_window = ProjectScheduleWindow
        self.assignment_window = AssignmentWindow

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
            self.window, width=25, text="Assignment Form",
            command=self.assignment_window
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
        self.main_window = tkinter.Tk()
        self.main_window.wm_title("Project Schedule Hub")

        # Initialize project variables.
        self.proj_date = None
        self.proj_descrpt = None
        self.proj_estdatest = None
        self.proj_estdateend = None
        self.proj_estbudget = None
        self.proj_actdatest = None
        self.proj_actdateend = None
        self.proj_actcost = None

        tkinter.Label(self.main_window, width=50,
                      text="Please enter project information below:").grid(
            pady=10, column=1, row=0
        )

        # Options for project selection.
        tkinter.Label(self.main_window, text="Customer Name").grid(
            pady=10, column=1, row=4
        )
        self.customer_name = tkinter.Entry(self.main_window)
        self.customer_name.grid(
            pady=10, column=2, row=4
        )

        tkinter.Label(self.main_window, text="Project Date").grid(
            pady=10, column=1, row=6
        )
        self.proj_date = tkinter.Entry(self.main_window)
        self.proj_date.grid(
            pady=10, column=2, row=6
        )

        tkinter.Label(self.main_window, text="Project Description").grid(
            pady=10, column=1, row=7
        )
        self.proj_descrpt = tkinter.Entry(self.main_window)
        self.proj_descrpt.grid(
            pady=10, column=2, row=7
        )

        tkinter.Label(self.main_window, text="Estimated Start Date").grid(
            pady=10, column=1, row=8
        )
        self.proj_estdatest = tkinter.Entry(self.main_window)
        self.proj_estdatest.grid(
            pady=10, column=2, row=8
        )

        tkinter.Label(self.main_window, text="Estimated End Date").grid(
            pady=10, column=1, row=9
        )
        self.proj_estdateend = tkinter.Entry(self.main_window)
        self.proj_estdateend.grid(
            pady=10, column=2, row=9
        )

        tkinter.Label(self.main_window, text="Estimated Budget").grid(
            pady=10, column=1, row=10
        )
        self.proj_estbudget = tkinter.Entry(self.main_window)
        self.proj_estbudget.grid(
            pady=10, column=2, row=10
        )

        tkinter.Label(self.main_window, text="Actual Start Date").grid(
            pady=10, column=1, row=11
        )
        self.proj_actdatest = tkinter.Entry(self.main_window)
        self.proj_actdatest.grid(
            pady=10, column=2, row=11
        )

        tkinter.Label(self.main_window, text="Actual End Date").grid(
            pady=10, column=1, row=12
        )
        self.proj_actdateend = tkinter.Entry(self.main_window)
        self.proj_actdateend.grid(
            pady=10, column=2, row=12
        )

        tkinter.Label(self.main_window, text="Actual Cost").grid(
            pady=10, column=1, row=13
        )
        self.proj_actcost = tkinter.Entry(self.main_window)
        self.proj_actcost.grid(
            pady=10, column=2, row=13
        )

        # Submit button.
        tkinter.Button(self.main_window, text="Submit",
                       command=self.submit_data).grid(
            pady=10, column=1, row=14
        )

        tkinter.Button(self.main_window, text="Quit",
                       command=self.quit).grid(
            pady=10, column=2, row=14
        )

        self.main_window.mainloop()

    def submit_data(self):
        """
        This function submits user submitted entries about the project of
        interest to the database.

        :return: TBD.
        """

        database = Database()
        project_data = []

        project_entries = ["",
                           "",
                           "",
                           self.proj_date.get(),
                           self.proj_descrpt.get(),
                           self.proj_estdatest.get(),
                           self.proj_estdateend.get(),
                           self.proj_estbudget.get(),
                           self.proj_actdatest.get(),
                           self.proj_actdateend.get(),
                           self.proj_actcost.get()]

        index = 0
        num_filled = 0
        for item in project_entries:
            if item == "":
                project_entries[index] = None
            else:
                num_filled += 1
            index += 1

        cus_name = self.customer_name.get()

        if num_filled == 0 and cus_name == "":
            ErrorMessageWindow("You have to fill in at least one argument!")
        else:
            # If a customer name is provided.
            if cus_name != "":
                customer_data = database.query_customer(cus_name=cus_name)
                if customer_data:
                    project_entries[1] = customer_data[0][0]
                    project_data = database.query_project(
                        project_query_options=project_entries)
                else:
                    ErrorMessageWindow("No customer with this name found.")
            else:
                project_data = database.query_project(
                    project_query_options=project_entries)

            if project_data:
                schedule_data = database.query_project_tasks(
                    project_data=project_data)
                customer_data = database.query_customer(project_data[0][1])
                region_data = database.query_region_id(customer_data[0][1])

                # Project schedule window definition.
                ps_window = tkinter.Tk()
                ps_window.wm_title("Project Schedule Display")
                tkinter.Label(
                    ps_window, text="Project Information:"
                ).grid()

                # Display project information.
                tkinter.Label(
                    ps_window,
                    text="Project ID: {}".format(project_data[0][0]),
                ).grid(
                    pady=5, column=0, row=1
                )
                tkinter.Label(
                    ps_window,
                    text="Description: {}".format(project_data[0][4]),
                ).grid(
                    pady=5, column=1, row=1
                )
                tkinter.Label(
                    ps_window,
                    text="Company: {}".format(customer_data[0][2]),
                ).grid(
                    pady=5, column=0, row=2
                )
                tkinter.Label(
                    ps_window,
                    text="Contract Date: {}".format(project_data[0][3]),
                ).grid(
                    pady=5, column=1, row=2
                )
                tkinter.Label(
                    ps_window,
                    text="Region: {}".format(region_data[0][1]),
                ).grid(
                    pady=5, column=2, row=2
                )
                tkinter.Label(
                    ps_window,
                    text="Start Date: {}".format(project_data[0][5]),
                ).grid(
                    pady=5, column=0, row=3
                )
                tkinter.Label(
                    ps_window,
                    text="End Date: {}".format(project_data[0][6]),
                ).grid(
                    pady=5, column=1, row=3
                )
                tkinter.Label(
                    ps_window,
                    text="Budget: ${}".format(project_data[0][7]),
                ).grid(
                    pady=5, column=2, row=3
                )

                # Schedule table definition.
                p_s_view = tkinter.ttk.Treeview(ps_window)
                p_s_view.grid(pady=10, column=1, row=5)

                p_s_view["show"] = "headings"
                p_s_view["columns"] = (
                    "Start Date", "End Date", "Task Description",
                    "Skill(s) Required", "Quantity Required"
                )

                # Table column headings.
                for heading in p_s_view["columns"]:
                    p_s_view.heading(heading, text=heading)
                    p_s_view.column(heading, width=250)

                # Load data into table.
                for item in schedule_data:
                    p_s_view.insert('', 'end', values=item)
            else:
                ErrorMessageWindow("No project found with given info.")

    def quit(self):
        self.main_window.destroy()


# -----------------------------------------------------------------------------


class AssignmentWindow:
    """
    This class represents the assignment window.
    """

    def __init__(self):
        self.database = Database()
        self.main_window = tkinter.Tk()
        self.main_window.wm_title("Assignment Hub")

        # Initialize project variables.
        self.project_entries = []
        self.proj_date = ""
        self.proj_descrpt = ""
        self.proj_estdatest = ""
        self.proj_estdateend = ""
        self.proj_estbudget = ""
        self.proj_actdatest = ""
        self.proj_actdateend = ""
        self.proj_actcost = ""

        # Initialize employee variables.
        self.employee_entries = []
        self.emp_lname = ""
        self.emp_mi = ""
        self.emp_fname = ""
        self.emp_hiredate = ""

        tkinter.Label(self.main_window, width=50,
                      text="Please enter project information below:").grid(
            pady=10, column=1, row=0
        )

        # Options for project selection.
        tkinter.Label(self.main_window, text="Customer Name").grid(
            pady=10, column=1, row=4
        )
        self.customer_name = tkinter.Entry(self.main_window)
        self.customer_name.grid(
            pady=10, padx=5, column=2, row=4
        )

        tkinter.Label(self.main_window, text="Project Date").grid(
            pady=10, column=1, row=6
        )
        self.proj_date = tkinter.Entry(self.main_window)
        self.proj_date.grid(
            pady=10, padx=5, column=2, row=6
        )

        tkinter.Label(self.main_window, text="Project Description").grid(
            pady=10, column=1, row=7
        )
        self.proj_descrpt = tkinter.Entry(self.main_window)
        self.proj_descrpt.grid(
            pady=10, padx=5, column=2, row=7
        )

        tkinter.Label(self.main_window, text="Estimated Start Date").grid(
            pady=10, column=1, row=8
        )
        self.proj_estdatest = tkinter.Entry(self.main_window)
        self.proj_estdatest.grid(
            pady=10, padx=5, column=2, row=8
        )

        tkinter.Label(self.main_window, text="Estimated End Date").grid(
            pady=10, column=1, row=9
        )
        self.proj_estdateend = tkinter.Entry(self.main_window)
        self.proj_estdateend.grid(
            pady=10, padx=5, column=2, row=9
        )

        tkinter.Label(self.main_window, text="Estimated Budget").grid(
            pady=10, column=1, row=10
        )
        self.proj_estbudget = tkinter.Entry(self.main_window)
        self.proj_estbudget.grid(
            pady=10, padx=5, column=2, row=10
        )

        tkinter.Label(self.main_window, text="Actual Start Date").grid(
            pady=10, column=1, row=11
        )
        self.proj_actdatest = tkinter.Entry(self.main_window)
        self.proj_actdatest.grid(
            pady=10, padx=5, column=2, row=11
        )

        tkinter.Label(self.main_window, text="Actual End Date").grid(
            pady=10, column=1, row=12
        )
        self.proj_actdateend = tkinter.Entry(self.main_window)
        self.proj_actdateend.grid(
            pady=10, padx=5, column=2, row=12
        )

        tkinter.Label(self.main_window, text="Actual Cost").grid(
            pady=10, column=1, row=13
        )
        self.proj_actcost = tkinter.Entry(self.main_window)
        self.proj_actcost.grid(
            pady=10, padx=5, column=2, row=13
        )

        # Options for employee information.

        tkinter.Label(self.main_window,
                      text="Or, enter a specific employee below:").grid(
            pady=10, column=1, row=14
        )

        tkinter.Label(self.main_window, text="Employee Last Name").grid(
            pady=10, column=1, row=15
        )
        self.emp_lname = tkinter.Entry(self.main_window)
        self.emp_lname.grid(
            pady=10, padx=5, column=2, row=15
        )

        tkinter.Label(self.main_window, text="Employee Middle Initial").grid(
            pady=10, column=1, row=16
        )
        self.emp_mi = tkinter.Entry(self.main_window)
        self.emp_mi.grid(
            pady=10, padx=5, column=2, row=16
        )

        tkinter.Label(self.main_window, text="Employee First Name").grid(
            pady=10, column=1, row=17
        )
        self.emp_fname = tkinter.Entry(self.main_window)
        self.emp_fname.grid(
            pady=10, padx=5, column=2, row=17
        )

        tkinter.Label(self.main_window, text="Employee Hire Date").grid(
            pady=10, column=1, row=18
        )
        self.emp_hiredate = tkinter.Entry(self.main_window)
        self.emp_hiredate.grid(
            pady=10, padx=5, column=2, row=18
        )

        # Submit and Quit Button.
        tkinter.Button(self.main_window, text="Submit",
                       command=self.submit_action).grid(
            pady=10, column=1, row=19
        )
        tkinter.Button(self.main_window, text="Quit",
                       command=self.quit).grid(
            pady=10, column=2, row=19
        )

    @staticmethod
    def check_input_empty(user_inputs):
        """
        This method checks whether if the data input by user is
        empty. It also sets empty fields to None.

        :param user_inputs: User input data collection. A list of strings.
        :return: A is_empty boolean and the modified user input collection.
        """

        is_empty = True
        index = 0
        for item in user_inputs:
            if item == "":
                user_inputs[index] = None
            else:
                is_empty = False
            index += 1

        return is_empty, user_inputs

    def gather_project_entries(self):
        """
        Collects project inputs from user.

        :return: A boolean whether if the collection is empty or not,
        The modified user input collection.
        """

        user_inputs = [
            self.customer_name.get(), self.proj_date.get(),
            self.proj_descrpt.get(), self.proj_estdatest.get(),
            self.proj_estdateend.get(), self.proj_estbudget.get(),
            self.proj_actdatest.get(), self.proj_actdateend.get(),
            self.proj_actcost.get()
        ]

        return self.check_input_empty(user_inputs)

    def gather_employee_entries(self):
        """
        Collects employee inputs from user.

        :return: A boolean whether if the collection is empty or not,
        The modified user input collection.
        """
        user_inputs = [
            self.emp_lname.get(), self.emp_mi.get(), self.emp_fname.get(),
            self.emp_hiredate.get()
        ]

        return self.check_input_empty(user_inputs)

    def submit_action(self):
        project_is_empty, project_inputs = self.gather_project_entries()
        employee_is_empty, employee_inputs = self.gather_employee_entries()

        if project_is_empty is True and employee_is_empty is True:
            ErrorMessageWindow("You must enter data into at least one field.")
        elif project_is_empty is True and employee_is_empty is False:
            ErrorMessageWindow("You must specify a project for this employee.")
        else:
            # Initialize project data for query.
            project_query_data = []
            sentinel = 0
            for i in range(3):
                project_query_data.append(None)
            for item in project_inputs:
                if sentinel > 0:
                    project_query_data.append(item)
                sentinel += 1

            if self.customer_name.get() != "":
                project_query_data[1] = self.database.query_customer(
                    cus_name=self.customer_name.get()
                )[0][0]

            # Initialize employee data for query.
            employee_query_data = []
            for i in range(2):
                employee_query_data.append(None)
            for item in employee_inputs:
                employee_query_data.append(item)

            project_data, employee_data = None, None

            if project_is_empty is False:
                project_data = self.database.query_project(project_query_data)
                if project_data:
                    if employee_is_empty is False:
                        employee_data = self.database.query_employee(
                            employee_query_data)

                    self.show_project_assignment(project_data, employee_data)
                else:
                    ErrorMessageWindow("Project not found.")

    def show_project_assignment(self, project_data, employee_data):
        pa_table = tkinter.Tk()
        pa_table.wm_title("Project Assignment Result Window")

        customer_data = self.database.query_customer(project_data[0][1])
        proj_id = project_data[0][0]
        if employee_data is not None:
            emp_id = employee_data[0][0]
            assignment_data = self.database.query_assignment(project_id=proj_id,
                                                             emp_id=emp_id)
        else:
            assignment_data = self.database.query_assignment(project_id=proj_id)

        tkinter.Label(
            pa_table, text="Project Information:"
        ).grid()

        # Display project information.
        tkinter.Label(
            pa_table,
            text="Project ID: {} {} Description: {}".format(
                project_data[0][0],
                "                ",
                project_data[0][4]
            ),
        ).grid(
            pady=5, column=0, row=1
        )
        tkinter.Label(
            pa_table,
            text="Company: {} {} Contract Date: {}".format(
                customer_data[0][2],
                "                ",
                project_data[0][3]
            ),
        ).grid(
            pady=5, column=0, row=2
        )

        # Assignment table definition.
        assignment_table = tkinter.ttk.Treeview(pa_table)
        assignment_table.grid(pady=5, column=0, row=4)

        assignment_table["show"] = "headings"
        assignment_table["columns"] = (
            "Task Starts", "Task Ends", "Task Info", "Skill Info",
            "Assignment ID", "Last Name", "First Name", "Assignment Starts",
            "Assignment Ends"
        )

        # Table headings.
        for heading in assignment_table["columns"]:
            assignment_table.heading(heading, text=heading)
            assignment_table.column(heading, width=150)

        # Load data into table.
        for item in assignment_data:
            assignment_table.insert('', 'end', values=item)

    def quit(self):
        """
        This method closes the assignment submission window.
        :return: Nothing.
        """

        self.main_window.destroy()


# -----------------------------------------------------------------------------

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


class SuccessMessageWindow:
    """
    This class represents a generic success message window that pops whenever
    a user input results in success.
    """

    def __init__(self, message):
        self.window = tkinter.Tk()
        self.window.wm_title("SUCCESS")

        self.success_msg = message
        tkinter.Label(self.window, text=self.success_msg).pack(
            pady=10, padx=10
        )

        tkinter.Button(
            self.window, text="Quit", command=self.window.destroy
        ).pack()


class MultiRowScreen:
    """
    This class returns a screen displaying a multi-row fetchall result
    for reference.
    """

    def __init__(self, incoming_data, data_type_name):
        self.data_type_name = data_type_name
        self.data = incoming_data
        self.main_window = tkinter.Tk()
        self.main_window.wm_title("Data Display")

        # Get how many columns exist in this data collection.
        num_columns = len(self.data[0])

        self.main_label = tkinter.Label(
            self.main_window,
            text="Your operation returned multiple rows for {}. "
                 "Please enter information again of {} of "
                 "your choice.".format(self.data_type_name,
                                       self.data_type_name))
        self.main_label.grid(pady=5, column=0, row=0)

        # Table definition.
        self.table = tkinter.ttk.Treeview(self.main_window)
        self.table.grid(pady=5, column=0, row=1)

        for i in range(num_columns):
            self.table.heading(i, text="'{}'".format(i))
            self.table.column(i)

        for item in self.data:
            self.table.insert('', 'end', values=item)

        self.main_window.mainloop()


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
            self.homePageWindow, width=25, text="Update",
            command=self.update_window
        ).grid(
            pady=10, column=1, row=3
        )
        tkinter.Button(
            self.homePageWindow, width=25, text="Quit",
            command=self.homePageWindow.destroy
        ).grid(
            pady=10, column=1, row=4
        )

        self.homePageWindow.mainloop()


mainPage = HomePage()
# mainPage.database.dbCursor.close()
# mainPage.database.dbConnection.close()
