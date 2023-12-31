"""_summary_ : Frame that collects details for a database connection
"""

# Import the necessary modules
import tkinter as tk
from tkinter import ttk


# Opener as a toplevel
class Connector(tk.Toplevel):
    """_summary_ : Frame that collects details for a database connection
    """

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent, width=500, height=100)

        # controller
        self.controller = parent
        # resizable false
        self.resizable(False, False)
        # self.overrideredirect(True)
        self.transient(parent)
        # title
        self.title("Connect a database")
        self.open_database_form()
        # change close button function
        self.protocol("WM_DELETE_WINDOW", self.dispose)

    def dispose(self):
        """_summary_ : dispose of the toplevel
                        and clear all fields
        """
        # dispose of the toplevel
        self.destroy()

    # add a database form
    def open_database_form(self):
        """_summary_ : get the db_type, db_user, db_pass, db_host, db_port, and db_name
                        through a form like view and create a connection to the database
        """
        dbs_conn_string_label = tk.Label(self, text="Connection String")
        dbs_conn_string_label.place(relx=0.25, rely=0.2, anchor="center")
        dbs_conn_string_entry = ttk.Entry(self,)
        dbs_conn_string_entry.place(anchor="center",
                                    relwidth=0.8,
                                    relheight=0.1,
                                    relx=0.5,
                                    rely=0.45,
                                    height=17)

        def create_database(e):
            """_summary_ : creates a database
            """
            # get the values from the entry boxes
            _conn_string = dbs_conn_string_entry.get()

            # check if the values are not empty
            if _conn_string != "":
                # create the database
                connected = self.controller.db_manager.connect(_conn_string)
                if connected:
                    # refresh the view
                    self.controller.sidebar.refresh()
                    # open a query window
                    # self.controller.main_view.add_tab(tab_name="Query", tab_type="query")
                    # close the window
                    self.dispose()
                # close the window
                self.dispose()
            else:
                pass


        # buttons
        open_database_button = tk.Button(self, text="Connect")
        open_database_button.place(relx=0.5, rely=0.8, anchor="center")
        open_database_button.bind("<Button-1>", create_database)
        # bind the enter key to the create_database function
        dbs_conn_string_entry.bind("<Return>", create_database)
