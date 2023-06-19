"""_summary_ : Frame shown when "databases" is selected in the sidebar,
                shows the list of databases in a grid and allows the user to
                select one the selected database is then passed to the central
                view from the sidebar
"""

# Import the necessary modules
import tkinter as tk
from tkinter import ttk

# Import the necessary classes
from ..popups.menu_frame import MenuFrame


class DbsPage(tk.Frame):
    """_summary_ : Frame shown when "databases" is selected in the sidebar,
                    shows the list of databases in a grid and allows the user to
                    select one the selected database is then passed to the central
                    view from the sidebar

    """

    def __init__(self, parent, db_list: list = None):
        """
            The __init__ function is called when the class is instantiated.
            It sets up the attributes of an object, and does any other necessary
            initialization.  The self parameter (you could choose any other name, but nobody ever does!)
            is automatically set to reference the newly-created object that needs to be initialized.

            :param self: Represent the instance of the class
            :param parent: Pass the controller to the class
            :param db_list: list: Pass the list of databases to the frame
            :return:  object
        """
        tk.Frame.__init__(self, parent, width=500, padx=5, pady=5)
        # controller
        self.controller = parent
        self.db_list = db_list
        # button to create a new database
        self.new_db_button = tk.Button(self, text="Create Database")
        self.new_db_button.place(x=5, y=60)
        self.new_db_button.bind("<Button-1>", self.controller.add_database_frame)
        # button to refresh the view

        # label for the page
        self.label = tk.Label(self, text="Databases ", font=("Arial", 30), bg="grey", justify="left")
        self.label.place(y=0, relx=0.5, relwidth=0.98, anchor="n")

        # extra frame(for refresh purposes)
        self.extra_frame = None

        # database list
        self.grid_view()

    # noinspection PyTypeChecker
    def grid_view(self):
        """
            The grid_view function is used to display the list of databases in a grid.
            It uses the get_database_details function from controller.py to retrieve all database details
            and then displays them in a treeview widget.

            :param self: Represent the instance of the object that calls the method
            :return: A frame with a treeview that displays the list of databases
                    and the number of tables in each database
        """

        # get database details
        _dbm = {}

        # use dictionary comprehension
        if self.db_list is not None:
            _dbm = {db: self.controller.controller.get_database_details(database_name=db) for db in self.db_list}

        self.extra_frame = tk.Frame(self, width=500, height=600, bg="white", borderwidth=2,
                                    relief="groove", padx=5, pady=5)
        self.extra_frame.place(y=140, height=650, bordermode="outside", relx=0.5, anchor="n", relwidth=0.98)
        treeview_frame = tk.Frame(self.extra_frame, padx=5, pady=5, bg="white")
        treeview_frame.pack(fill="both", expand=True)

        # treeview
        treeview = ttk.Treeview(treeview_frame)
        treeview.pack(fill="both", expand=True)
        treeview["columns"] = ("one",)
        treeview.column("#0", width=270, minwidth=270, stretch=tk.NO)
        treeview.column("one", width=150, minwidth=150, stretch=tk.NO)
        treeview.heading("#0", text="Database Name", anchor=tk.W)
        treeview.heading("one", text="Tables Count", anchor=tk.W)
        # insert data
        row_num = 1
        if _dbm is not None:
            for key, value in _dbm.items():
                for k, v in value.items():
                    treeview.insert(parent="", index="end", iid=str(row_num), text=v["name"],
                                    values=(v["tables_length"]))

                row_num += 1

        # menu popup
        treeview.bind(
            "<Button-3>",
            lambda e: open_menu_frame(e))
        # bind the treeview to the change sidebar selection function to the database name
        treeview.bind(
            "<Button-1>",
            lambda e: self.controller.controller.sidebar.change_selected_item(
                str(treeview.item(treeview.selection(), "text"))))

        # function to add the menu frame to the main view
        def open_menu_frame(event):
            """
                The open_menu_frame function is called when the user right-clicks on a treeview item.
                It opens a popup menu that allows the user to delete or edit an item.

                :param event: Identify the event that caused the function to be called
                :return: A menu frame object
            """
            # identify the treeview item that was clicked
            menu_frame = None
            item = treeview.identify_row(event.y)
            # trigger treeview focus
            tr = str(treeview.item(item, "text"))
            if item:
                # activate the top level window
                try:
                    menu_frame = MenuFrame(self.controller, db_name=tr, hide_alter=True)
                    menu_frame.tk_popup(event.x_root, event.y_root)
                    # get focus
                    menu_frame.focus_set()
                finally:
                    menu_frame.grab_release()
