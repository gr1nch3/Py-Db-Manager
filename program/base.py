"""_summary_: base frame for the tkinter program that contains a sidebar,
                a central view, and an overlay view for database choosing
"""

# Import the necessary modules
import tkinter as tk
import logging

# Import the necessary classes
from .database import Database
from .sidebar_view import Sidebar
from .central_view import CentralView
from .error_handler import ErrorHandler
from program.popups.open_database_frame import Opener
from program.popups.menu_frame import MenuFrame


# noinspection PyUnusedLocal
class BaseView(tk.Tk):
    """_summary_: base frame for the tkinter program that contains a sidebar,
                    a central view, and an overlay view for database choosing

    Args:
        tk (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        """
            The __init__ function is called when the class is instantiated.
            It sets up the instance of the class, and makes it ready for use.
            The __init__ function can take arguments, but self is always required as
            the first argument (it refers to the newly created instance).

            :param self: Represent the instance of the class
            :param *args: Send a non-keyword variable length argument list to the function
            :param **kwargs: Pass keyword, variable-length argument list
            :return: None
        """
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Py-Db Manager")
        # Configure the logger
        logging.basicConfig(filename='logs/database_manager.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.wm_attributes("-zoomed", True)
        width = self.winfo_screenwidth()  # 100
        height = self.winfo_screenheight()  # 100
        self.geometry(f"{width}x{height}+0+0")  # Fullscreen
        # adding icon
        icon_image = tk.PhotoImage(file="program/images/icon_img.png")
        self.iconphoto(False, icon_image)

        # current database
        self.current_database = None

        # sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.pack(side="left", fill="y")

        # central view
        self.central_view = CentralView(self)
        self.central_view.pack(fill="both", expand=True)

        # open database view (overlay)
        self.open_database_view = None

        # menu frame
        self.menu_frame = MenuFrame(self)

        # bind esc key to close program
        self.bind("<Escape>", lambda event: self.destroy())

    # function to refresh the sidebar and central view
    def refresh(self):
        """
            The refresh function is called when the user add on a new item in the sidebar.
            It refreshes the sidebar and the central view.

            :param self: Represent the instance of the class
            :return: None
        """
        # refresh the sidebar
        self.sidebar.refresh()

    # function to add the open database view to the main view
    def open_database_frame(self, event):
        """
            The open_database_frame function is called when the user clicks on the &quot;Open Database&quot; button.
            It opens a new window that allows the user to input details including the authentication, host, port,
            database name etc. to create a new connection string and access the database.

            :param self: Represent the instance of the class
            :param event: Pass the event that triggered the function
            :return: The opener class
        """
        # activate the top level window
        self.open_database_view = Opener(self)
        self.open_database_view.deiconify()
        self.open_database_view.focus_set()

    # function to open a database
    def open_database(self, database_type, host, port, username, password, database=None):
        """
            The open_database function is used to connect to a database.

            :param database_type: Specify the type of database you want to connect to
            :param host: Specify the hostname or ip address of the database server
            :param port: Specify the port number for the database connection
            :param username: Connect to the database
            :param password: Pass in the password for the database
            :param database: Specify the name of the database to connect to
            :return: A database object
        """
        database = database if database else ""

        database_type = database_type.lower()
        # convert port to int
        port = int(port)

        try:
            # create a database object
            database = Database(db_type=database_type, db_host=host, db_port=port, db_user=username, db_pass=password,
                                db_name=database)
            database.connect()
        except Exception as e:
            ErrorHandler(self, str(e))

    # # function to add a database
    def add_database(self, conn_string, db_name):
        """
            The add_database function is used to add a database.

            :param conn_string: Specify the connection string for the database
            :param db_name: Specify the name of the database to connect to
            :return: A database object
        """
        # get the values from the connection string mysql://root:9r06r4m3rM#@localhost:3306/
        conn_string = str(conn_string)

        database_type = ""
        database_user = ""
        database_pass = ""
        database_host = ""
        database_port = 0

        # check the amount of colons in the string
        if conn_string.count(":") == 3:
            database_type = conn_string.split("://")[0]
            database_user = conn_string.split("://")[1].split(":")[0]
            database_pass = conn_string.split("://")[1].split(":")[1].split("@")[0]
            database_host = conn_string.split("://")[1].split(":")[1].split("@")[1]
            database_port = int(str(conn_string.split("://")[1].split(":")[2]))
        elif conn_string.count(":") == 2:
            print("no password")
            # there's no password, so the string will only have 2 colons
            # get the values from the connection string mysql://root@localhost:3306/
            database_type = conn_string.split("://")[0]
            database_user = conn_string.split("://")[1].split("@")[0]
            database_pass = ""
            database_host = conn_string.split("://")[1].split("@")[1].split(":")[0]
            database_port = int(str(conn_string.split("://")[1].split(":")[1]))



        # create a database object
        try:
            database = Database(db_type=database_type, db_host=database_host, db_port=database_port,
                                db_user=database_user, db_pass=database_pass,
                                db_name=db_name)
            database.create_database()
            database.connect()
        except Exception as e:
            ErrorHandler(self, str(e))

    # function to get a database details based on the database name
    def get_database_details(self, database_name):
        """
            The get_database_details function takes a database name as input and returns the details of that database.
            The function uses the process_conn_string function to get the connection string for that particular
            database.
            It then creates an object of Database class, connects to it and gets its metadata
            using get_db_metadata() method.

            :param self: Represent the instance of the class
            :param database_name: Get the database details from the process_conn_string function
            :return: A list of the database details
        """

        # get the database details
        database_details = self.process_conn_string(database_name)

        try:
            db = Database(db_type=database_details[0],
                          db_name=database_details[1],
                          db_user=database_details[2],
                          db_pass=database_details[3],
                          db_host=database_details[4],
                          db_port=database_details[5])
            db.connect()
            data = db.get_db_metadata()
            db.disconnect()
            print("data", data)
            return data
        except Exception as e:
            ErrorHandler(self, str(e))

    # function to get the list of databases and pass them to the sidebar
    @staticmethod
    def get_databases():
        """
            It creates an object of the Database class and calls the get_databases() method to get
            the dict of databases.
            :return: A list of the databases available to the user
        """
        temp_db = Database(db_type="")
        val = temp_db.get_databases()

        # TODO: add option to return a list or dict via a parameter and use of process_conn_string within this function
        return val

    # get the connection string of the database
    def process_conn_string(self, db_name):
        """
            The process_conn_string function takes a database name as an argument and returns
            the connection string for that database.

            :param self: Represent the instance of the class
            :param db_name: Find the database name in the dictionary
            :return: The connection string for a database
        """
        all_dict = self.get_databases()

        # use list comprehension to find the database name
        db_conn_string = [
            value3
            for key, value in all_dict.items()
            for key2, value2 in value.items()
            for item in value2
            if item == db_name
            for key3, value3 in value2.items()
            if key3 == db_name
        ]

        if len(db_conn_string) > 0:
            return db_conn_string[0]
        else:
            return None

    # set current database
    def set_current_database(self, database: list = None):
        """
            The set_current_database function is used to set the current database that will be used for all subsequent
            database operations. The function takes a list of parameters as an argument,
                                    and uses those parameters to create a
            Database object. If no arguments are passed in, then the current_database attribute is set to None.

            :param self: Represent the instance of the class
            :param database: list: Pass in the database list that is created when a user adds a new database
            :return: The current database
        """
        if database is None:
            self.current_database = None
            return self.current_database
        else:
            # get the variables from the list
            database_type, database_name, username, password, host, port = database[0], database[1], database[2], \
                database[3], database[4], database[5]

            self.current_database = Database(db_type=database_type, db_host=host, db_port=port, db_user=username,
                                             db_pass=password, db_name=database_name)
            return self.current_database

    # delete a database
    def delete_database(self, database_name=None):
        """
            The delete_database function deletes a database on the server.

            :param self: Represent the instance of the class
            :param database_name: str: Pass in the database list that is created when a user adds a new database
            :return: Nothing
        """
        # get the database details
        database_details = self.process_conn_string(database_name)

        db = Database(db_type=database_details[0],
                      db_name=database_details[1],
                      db_user=database_details[2],
                      db_pass=database_details[3],
                      db_host=database_details[4],
                      db_port=database_details[5])
        try:
            db.connect()
            # remove the database from the list of databases
            db.query(f"DROP DATABASE IF EXISTS {database_name}", as_transaction=True)
            db.remove_connection_string()
            db.disconnect()
            self.refresh()
        except Exception as e:
            ErrorHandler(self, str(e))

    # renaming database
    def alter_database(self, current_db_name, new_db_name):
        """
            The rename_database function renames a database on the server.

            :param self: Represent the instance of the class
            :param current_db_name: The current name of the database
            :param new_db_name: The new name of the database
        """
        # get the database details
        database_details = self.process_conn_string(current_db_name)

        try:
            db = Database(db_type=database_details[0],
                          db_name=database_details[1],
                          db_user=database_details[2],
                          db_pass=database_details[3],
                          db_host=database_details[4],
                          db_port=database_details[5])
            db.connect()

            # check db type before running the query
            if db.db_type == "mssql":
                db.query(f"ALTER DATABASE {current_db_name} MODIFY NAME = {new_db_name}")
            elif db.db_type == "mysql":
                q = f"ALTER DATABASE {current_db_name} RENAME TO {new_db_name}"
                db.query(str(q))
            elif db.db_type == "postgresql":
                db.query(f"ALTER DATABASE {current_db_name} RENAME TO {new_db_name}")
            else:
                pass
            db.disconnect()
            self.refresh()
        except Exception as e:
            ErrorHandler(self, str(e))

    # adding table to database
    def add_table(self, table_name, columns, database: Database = None):
        """
            The add_table function adds a table to a database on the server.

            :param self: Represent the instance of the class
            :param table_name: The name of the table to be added
            :param columns: The columns to be added to the table
            :param database: Database object: The database to add the table to
        """

        if database is not None:
            try:
                db = database
                db.connect()

                # check db type before running the query
                if db.db_type == "mssql":
                    db.query(f"CREATE TABLE {table_name} {columns};")
                elif db.db_type == "mysql":
                    db.query(f"CREATE TABLE {table_name} {columns};")
                elif db.db_type == "postgresql":
                    db.query(f"CREATE TABLE {table_name} {columns};")
                else:
                    pass
                db.disconnect()
                self.refresh()
            except Exception as e:
                ErrorHandler(self, str(e))

    # deleting a table
    def delete_table(self, table_name):
        """
            The delete_table function deletes a table from a database on the server.

            :param self: Represent the instance of the class
            :param table_name: The name of the table to be deleted
            :param table_name: The name of the table to be deleted
        """
        if self.current_database is not None:

            try:
                db = self.current_database
                db.connect()

                # check db type before running the query
                if db.db_type == "mssql":
                    db.query(f"DROP TABLE {table_name};")
                elif db.db_type == "mysql":
                    db.query(f"DROP TABLE {table_name};")
                elif db.db_type == "postgresql":
                    db.query(f"DROP TABLE {table_name};")
                else:
                    pass
                db.disconnect()
                self.refresh()
            except Exception as e:
                ErrorHandler(self, str(e))

    # altering a table
    def alter_table(self, table_name, change):
        """
            The alter_table function alters a table from a database on the server.

            :param self: Represent the instance of the class
            :param table_name: The name of the table to be altered
            :param change: The change to be made to the table
        """

        if self.current_database is not None:

            try:
                db = self.current_database
                db.connect()

                # check db type before running the query
                if db.db_type == "mssql":
                    db.query(change)
                else:
                    db.query(f"ALTER TABLE {str(table_name)} {str(change)};")

                db.disconnect()
                self.refresh()
            except Exception as e:
                ErrorHandler(self, str(e))

    # inserting data into a table
    def insert_to_table(self, table_name, columns, values):
        """
            The insert_data function inserts data into a table in a database on the server.

            :param self: Represent the instance of the class
            :param table_name: The name of the table to insert data into
            :param columns: The columns to insert data into
            :param values: The values to insert into the table
        """
        if self.current_database is not None:
            try:
                db = self.current_database
                db.connect()

                # check db type before running the query
                if db.db_type == "mssql":
                    db.query(f"INSERT INTO {table_name} {columns} VALUES {values};")
                elif db.db_type == "mysql":
                    db.query(f"INSERT INTO {table_name} {columns} VALUES {values};")
                elif db.db_type == "postgresql":
                    db.query(f"INSERT INTO {table_name} {columns} VALUES {values};")
                else:
                    pass
                db.disconnect()
                self.refresh()
            except Exception as e:
                ErrorHandler(self, str(e))

    # updating data in a table
    def update_table_row(self, table_name, change, condition):
        """
            The update_table function updates data in a table in a database on the server.

            :param self: Represent the instance of the class
            :param table_name: The name of the table to update data in
            :param change: The change to be made to the data in the table
            :param condition: The condition to update data in the table
        """

        if self.current_database is not None:
            try:
                db = self.current_database
                db.connect()

                # check db type before running the query
                if db.db_type == "mssql":
                    db.query(f"UPDATE {table_name} SET {change} WHERE {condition};")
                elif db.db_type == "mysql":
                    db.query(f"UPDATE {table_name} SET {change} WHERE {condition};")
                elif db.db_type == "postgresql":
                    db.query(f"UPDATE {table_name} SET {change} WHERE {condition};")
                else:
                    pass
                db.disconnect()
                self.refresh()
            except Exception as e:
                ErrorHandler(self, str(e))

    # deleting data from a table
    def delete_from_table(self, table_name, condition):
        """
            The delete_from_table function deletes data from a table in a database on the server.

            :param self: Represent the instance of the class
            :param table_name: The name of the table to delete data from
            :param condition: The condition to delete data from the table
        """
        if self.current_database is not None:
            try:
                db = self.current_database
                db.connect()

                # check db type before running the query
                if db.db_type == "mssql":
                    db.query(f"DELETE FROM {table_name} WHERE {condition};")
                elif db.db_type == "mysql":
                    db.query(f"DELETE FROM {table_name} WHERE {condition};")
                elif db.db_type == "postgresql":
                    db.query(f"DELETE FROM {table_name} WHERE {condition};")
                else:
                    pass
                db.disconnect()
                self.refresh()
            except Exception as e:
                ErrorHandler(self, str(e))
