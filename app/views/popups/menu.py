""" _Summary_ : This file contains the class MenuFrame, which is a frame that
                contains the menu for running queries or refreshing the database.
"""

# import necessary modules
import tkinter as tk

class Menufram(tk.Menu):
    """_summary_ : frame for the menu that pops up when a right-click is performed

    Args:
        tk (_type_): _description_
    """

    def __init__(self, parent, tearoff=0):
        """_summary_

        Args:
            parent (_type_): _description_
            tearoff (int, optional): _description_. Defaults to 0.
        """
        tk.Menu.__init__(self, parent, tearoff=tearoff)
        # controller
        self.controller = parent
        # close menu when clicked outside
        self.bind("<FocusOut>", lambda event: self.destroy())
        # self.add_command(label="Run", command=self._run)
        # self.add_command(label="Refresh", command=self._refresh)

    def _run(self):
        """_summary_ : runs the query
        """
        pass
        # self.controller.run_query()

    def _refresh(self):
        """_summary_ : refreshes the database
        """
        pass
        # self.controller.refresh_database()