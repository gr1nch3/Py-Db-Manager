"""_summary_ : Frame that collects details for a database connection
"""

# Import the necessary modules
import tkinter as tk
from tkinter import ttk


# Opener as a toplevel
# noinspection PyUnusedLocal
class DbCreator(tk.Toplevel):
    """_summary_ : Frame that collects details for a database connection
    """

    def __init__(self, parent):
        """
            The __init__ function is called when the class is instantiated.
            It sets up the initial state of the object, which in this case means
            setting up a reference to its parent (the root window), and creating
            a couple of instance variables that will be used later on. The first
            parameter passed to __init__ must always be self; it refers to the newly-created object itself.

            :param self: Represent the instance of the class
            :param parent: Pass the controller to the new window
            :return: An instance of the class
        """
        tk.Toplevel.__init__(self, parent, width=500, height=200)

        # controller
        self.controller = parent
        # resizable false
        self.resizable(False, False)
        # self.overrideredirect(True)
        self.transient(parent)
        # title
        self.title("Create a database")
        self.create_database_form()
        # change close button function
        self.protocol("WM_DELETE_WINDOW", self.dispose)

    def dispose(self):
        """
            The dispose function is called when the user closes the window.
            It removes all references to this object, so that it can be garbage collected.


            :param self: Represent the instance of the class
            :return: The toplevel
        """
        # dispose of the toplevel
        self.destroy()

    # add a database form
    def create_database_form(self):
        """
            The create_database_form function creates a form for the user to create a database.
            The function takes in no arguments and returns nothing. The function is called by the
            create_database method of the DatabasePage class.

            :param self: Refer to the instance of the class
            :return: A dictionary
        """
        def get_connection_strings():
            """
                The get_connection_strings function is used to get the connection strings from the database.json file
                and return them as a list of strings. The function takes no arguments and returns a list of strings.

                :return: A list of connection strings
            """
            _dbs = self.controller.controller.get_databases()
            sbar = self.controller.controller.sidebar
            selected = sbar.get_selected_item()

            _conn_strings = []

            # check if the selected is in the list of databases types
            if selected is not None:
                for k, v in _dbs.items():
                    if str(selected).lower() == str(k).lower():
                        for k2, v2 in v.items():
                            for k3, v3 in v2.items():
                                _conn_strings.append(v3)
                    else:
                        continue
            else:
                pass

            # change this: [['mysql', 'Supermarket', 'root', '9r06r4m3rM#', 'localhost', 3306]]
            # to this: ['mysql://root:9r06r4m3rM#@localhost:3306/Supermarket']
            _conn_strings = [f"{x[0]}://{x[2]}:{x[3]}@{x[4]}:{x[5]}" for x in _conn_strings]
            # filter _conn_strings and remove duplicates
            _conn_strings = list(dict.fromkeys(_conn_strings))
            return _conn_strings

        # function to create a database
        def create_database(event):
            """
                The create_database function is used to create a database. The function takes no arguments and returns
                nothing. The function is called by the create_database_form function.

                :return: None
            """
            # get the values from the entry boxes
            _conn_string = dbs_conn_string_entry.get()
            _database_name = database_name_entry.get()

            # check if the values are not empty
            if _conn_string != "" and _database_name != "":
                # create the database
                self.controller.controller.add_database(conn_string=_conn_string, db_name=_database_name)
                # close the window
                self.dispose()
                self.controller.controller.refresh()
            else:
                pass

        # connection strings combobox values
        cbvalues = get_connection_strings()

        # Combobox for the connection string
        dbs_conn_string_label = tk.Label(self, text="Connection String")
        dbs_conn_string_label.place(relx=0.25, rely=0.05, anchor="center")
        dbs_conn_string_entry = ttk.Combobox(self, values=cbvalues)
        dbs_conn_string_entry.place(anchor="center",
                                    relwidth=0.8,
                                    relheight=0.1,
                                    relx=0.5,
                                    rely=0.18,
                                    height=10)

        database_name_label = tk.Label(self, text="Database Name")
        database_name_label.place(relx=0.25, rely=0.4, anchor="center")
        database_name_entry = tk.Entry(self)
        database_name_entry.place(anchor="center",
                                  relwidth=0.5,
                                  relheight=0.1,
                                  relx=0.5,
                                  rely=0.55,
                                  height=10)

        # buttons
        open_database_button = tk.Button(self, text="Create Database")
        open_database_button.place(relx=0.5, rely=0.9, anchor="center")
        open_database_button.bind("<Button-1>", lambda e: create_database(e))
