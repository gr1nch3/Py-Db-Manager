"""_summary_ : base app manager
"""
# Import the necessary modules
import tkinter as tk
import logging

# Import the necessary classes
from database.database_manager import DatabaseManager
from .views.base import MainView
from .views.sidebar import Sidebar
from .views.popups.connect_db import Connector

class AppManager(tk.Tk):
    """_summary_

    Args:
        tk (_type_): _description_
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # -------------------------------- window attr ------------------------------- #
        self.wm_title("Py-Db")
        self.wm_attributes("-zoomed", True)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        # --------------------------- initiating essentials -------------------------- #
        self.db_manager = DatabaseManager()

        # ------------------------------- extra classes ------------------------------ #
        self.sidebar = Sidebar(self)
        self.sidebar.pack(side="left", fill="y")
        self.main_view = MainView(self, self.db_manager)
        self.main_view.pack(fill="both", expand=True)

        # open database view (overlay)
        self.open_database_view = None

        # --------------------------------- logging ---------------------------------- #
        logging.basicConfig(filename='logs/database_manager.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

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
        self.open_database_view = Connector(self)
        self.open_database_view.deiconify()
        self.open_database_view.focus_set()

        # open a query tab
        # self.main_view.add_tab(tab_type="query")
