"""_summary_: main view for the tkinter program that contains a sidebar,
                a central view, and an overlay view for database choosing
"""
# Import the necessary modules
import tkinter as tk

# Import the necessary classes
from .central_pages.detail_page import DetailPage
from .central_pages.dbs_page import DbsPage
from .central_pages.table_page import TablePage
from .popups.add_database_frame import DbCreator
from .popups.alter_table_frame import AlterTable
# from .popups.alter_database_frame import AlterDatabase
from .popups.add_table_frame import AddTable
from .popups.insert_frame import InsertFrame
from .popups.alter_row_frame import EditFrame


# noinspection PyUnusedLocal
class CentralView(tk.Frame):
    """_summary_: main view for the tkinter program that contains a sidebar,
    """

    def __init__(self, parent):
        """
            The __init__ function is called when the class is instantiated.
            It sets up the initial state of the object, which in this case means
            creating a reference to its parent (the controller), and setting up some
            instance variables that will be used throughout.

            :param self: Represent the instance of the class
            :param parent: Pass the controller object to the frame
            :return: The object itself
        """
        tk.Frame.__init__(self, parent, width=500)
        # controller
        self.controller = parent
        self.config(bg="blue")

        # var for the frame
        self._frame = tk.Frame(self)
        # create a label
        label = tk.Label(self._frame,
                         text="Welcome to the Database Management System",
                         # bg="#ffffff",
                         font=("Arial", 30))
        # pack the label
        label.pack(pady=100, padx=100)

        # display image
        img = tk.PhotoImage(file="program/images/icon_img.png")
        # resize the image
        img = img.subsample(2, 2)
        # create a label
        img_label = tk.Label(self._frame, image=img)
        img_label.image = img
        # pack the label
        img_label.pack(pady=100, padx=100)
        # pack the frame
        self._frame.pack(fill="both", expand=True)

        # create a database object (overlay)
        self.add_database_view = None

        # create an alter table object (overlay)
        self.alter_table_view = None

        # create an alter database object (overlay)
        self.alter_database_view = None

        # create an add table object (overlay)
        self.add_table_view = None

        # create an insert object (overlay)
        self.insert_view = None

        # create an edit object (overlay)
        self.edit_view = None

    # function to switch frame
    def switch_frame(self, class_name=None, db_list: list = None, table_name: str = None):
        """
            The switch_frame function is used to switch between the different frames in the application.
            It takes a class name as an argument and then creates an instance of that class,
            destroying any previous frame.
            The new frame is then packed into the window.

            :param self: Represent the instance of the class
            :param class_name: Determine which frame to switch to
            :param db_list: list: Pass the list of databases to the dbspage class
            :param table_name: str: Pass the name of the table to be displayed
            :return: The new frame that is created and set as the current frame
        """
        # self.controller.central_view = None
        if class_name == "TablePage":
            new_frame = TablePage(self, table_name=table_name)
        elif class_name == "DetailPage":
            new_frame = DetailPage(self)
        else:
            new_frame = DbsPage(self, db_list=db_list)
        # check if there is a frame
        if self._frame is not None:
            self._frame.destroy()
        # set the frame (not unbound)
        self._frame = new_frame
        # pack the frame
        self._frame.pack(fill="both", expand=True)

    # function to add the add database view to the main view
    def add_database_frame(self, event):
        """
            The add_database_frame function is called when the user clicks on the &quot;Add Database&quot; button.
            It creates a new instance of DbCreator, which is a Toplevel widget that contains all the
            widgets necessary to create and add a database to our application. It then deiconify this
            new window and sets focus on it.

            :param self: Represent the instance of the class
            :param event: Pass the event that triggered this function
            :return: The add_database_view
        """
        # pack the add database view# activate the top level window
        self.add_database_view = DbCreator(self)
        self.add_database_view.deiconify()
        self.add_database_view.focus_set()

    # function to add the alter table view to the main view
    def alter_table_frame(self, event, table_name: str):
        """
            The alter_table_frame function is called when the user clicks on the alter table button.
            It creates an instance of AlterTable and displays it to the user.

            :param self: Represent the instance of the class
            :param event: Pass the event that triggered this function
            :param table_name: str: Pass the name of the table to be altered
            :return: The alter table view
        """

        # pack the add database view# activate the top level window
        self.alter_table_view = AlterTable(self, table_name=table_name)
        self.alter_table_view.deiconify()
        self.alter_table_view.focus_set()

    # function to add the add table view to the main view
    def add_table_frame(self, event):
        """
            The add_table_frame function is called when the user clicks on the add table button.
            It creates an instance of AddTable and displays it to the user.

            :param self: Represent the instance of the class
            :param event: Pass the event that triggered this function
            :return: The add table view
        """

        # pack the add database view# activate the top level window
        self.add_table_view = AddTable(self, self.controller.current_database)
        self.add_table_view.deiconify()
        self.add_table_view.focus_set()

    # function to add the insert view to the main view
    def insert_frame(self, event, table_name: str):
        """
            The insert_frame function is called when the user clicks on the insert button.
            It creates an instance of InsertFrame and displays it to the user.

            :param self: Represent the instance of the class
            :param event: Pass the event that triggered this function
            :param table_name: str: Pass the name of the table to be inserted into
            :return: The insert view
        """

        # pack the add database view# activate the top level window
        self.insert_view = InsertFrame(self, table_name=table_name)
        self.insert_view.deiconify()
        self.insert_view.focus_set()

    # function to edit a row in the table
    def edit_row(self, event, table_name, row_value):
        """
            The edit_row function is called when the user clicks on the edit button.
            It creates an instance of EditFrame and displays it to the user.

            :param self: Represent the instance of the class
            :param event: Pass the event that triggered this function
            :param table_name: str: Pass the name of the table to be edited
            :param row_value: str: Pass the name of the table to be edited
            :return: The edit view
        """

        # pack the add database view# activate the top level window
        self.edit_view = EditFrame(self, table_name=table_name, row_value=str(row_value))
        self.edit_view.deiconify()
        self.edit_view.focus_set()

    def view(self):
        """
            The _view function is the default view for the central frame.
            it is a blank frame with a text in the center.

            :param self: Represent the instance of the class
        """
        # create a frame
        frame = tk.Frame(self, bg="#ffffff")
        # create a label
        label = tk.Label(frame, text="Welcome to the Database Management System", bg="#ffffff")
        # pack the label
        label.pack(pady=100, padx=100)
        # pack the frame
        frame.pack(fill="both", expand=True)
