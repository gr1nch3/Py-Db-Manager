"""_summary_ : Frame that collects details for a database connection
"""

# Import the necessary modules
import tkinter as tk
from tkinter import ttk


# Opener as a toplevel
class Opener(tk.Toplevel):
    """_summary_ : Frame that collects details for a database connection
    """

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent, width=500, height=300)

        # controller
        self.controller = parent
        # resizable false
        self.resizable(False, False)
        # self.overrideredirect(True)
        self.transient(parent)
        # title
        self.title("Open a database")
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
        # entry boxes and labels (designed  with entry boxes left and right and labels on top of the boxes)
        database_type_label = tk.Label(self, text="Database Type")
        database_type_label.place(relx=0.25, rely=0.15, anchor="center")
        database_type_entry = ttk.Combobox(self, values=["MySQL", "PostgreSQL", "MsSQL"])
        database_type_entry.place(relx=0.25, rely=0.25, anchor="center")

        database_user_label = tk.Label(self, text="Database User")
        database_user_label.place(relx=0.75, rely=0.15, anchor="center")
        database_user_entry = tk.Entry(self)
        database_user_entry.place(relx=0.75, rely=0.25, anchor="center")

        database_password_label = tk.Label(self, text="Database Password")
        database_password_label.place(relx=0.25, rely=0.4, anchor="center")
        database_password_entry = tk.Entry(self)
        database_password_entry.place(relx=0.25, rely=0.5, anchor="center")
        # database_password_entry.config(show="*")

        database_host_label = tk.Label(self, text="Database Host")
        database_host_label.place(relx=0.75, rely=0.4, anchor="center")
        database_host_entry = tk.Entry(self)
        database_host_entry.place(relx=0.75, rely=0.5, anchor="center")

        database_port_label = tk.Label(self, text="Database Port")
        database_port_label.place(relx=0.25, rely=0.65, anchor="center")
        database_port_entry = tk.Entry(self)
        database_port_entry.place(relx=0.25, rely=0.75, anchor="center")

        database_name_label = tk.Label(self, text="Database Name")
        database_name_label.place(relx=0.75, rely=0.65, anchor="center")
        database_name_entry = tk.Entry(self)
        database_name_entry.place(relx=0.75, rely=0.75, anchor="center")

        # get the values from the entry boxes and create a connection

        # noinspection PyUnusedLocal
        def open_database(event):
            """_summary_ : get the values from the entry boxes and create a connection
            """
            db_type = database_type_entry.get()
            host = database_host_entry.get()
            port = database_port_entry.get()
            user = database_user_entry.get()
            password = database_password_entry.get()
            database = database_name_entry.get()
            self.controller.open_database(db_type, host, port, user, password, database)
            # dispose of the toplevel
            self.controller.refresh()
            self.dispose()

        # buttons
        open_database_button = tk.Button(self, text="Open Database")
        open_database_button.place(relx=0.5, rely=0.9, anchor="center")
        open_database_button.bind("<Button-1>", lambda event: open_database(event))
