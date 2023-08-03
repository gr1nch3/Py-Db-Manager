""" _Summary_ : This file contains the class InsertFrame, which is a frame
                that pops up when the user wants to insert a row. It contains
                the following
                - column names
                - entry boxes for the user to enter the new column values
                - a button for submitting the changes

"""

# import necessary modules
import tkinter as tk
import tkinter.ttk as ttk


class InsertFrame(tk.Toplevel):
    """_summary_: frame for inserting a row
    """

    def __init__(self, parent, table_name: str):
        """
            The __init__ function is called when the class is being initiated.

            :param self: Represent the instance of the class
            :param parent: Pass the controller to insert frame
            :param table_name: Pass the table name to  insert frame
            :return: Nothing
        """
        tk.Toplevel.__init__(self, parent)
        # controller
        self.controller = parent
        # resizable false
        self.resizable(False, False)
        # self.overrideredirect(True)
        self.transient(parent)
        # database
        self._db = self.controller.controller.current_database
        # close menu when clicked outside
        # self.bind("<FocusOut>", lambda event: self.dispose())
        # change close button function
        self.protocol("WM_DELETE_WINDOW", self.dispose)
        # table name
        self.table_name = table_name
        # title
        self.title("Insert Row")
        # view
        self._view()

    def dispose(self):
        """
            The dispose function is called when the user closes the window.
            It removes all references to this object, so that it can be garbage collected.

            :param self: Represent the instance of the class
            :return: The toplevel
        """
        # dispose of the toplevel
        self.destroy()

    def _view(self):
        """
            The _view function is called when the class is being initiated.

            :param self: Represent the instance of the class
        """
        # connect to the database
        self._db.connect()

        # display the column names vertically in a grid and the entry boxes to the right
        display_frame = tk.Frame(self)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # get the column names
        # tuple(list(self._db.get_table_columns(str(self.table_name))))
        column_names = []

        # remove the auto increment column if True
        for column in self._db.get_table_columns(str(self.table_name)):
            if "autoincrement" in column and column["autoincrement"] is False:
                column_names.append(column["name"])
            elif "autoincrement" not in column:
                column_names.append(column["name"])

        column_names = tuple(column_names)

        self.column_inputs = []
        # create a label for each column name
        for i in range(len(column_names)):
            # label
            label = ttk.Label(display_frame, text=column_names[i])
            label.grid(row=i, column=0, sticky=tk.W)
            # entry box
            entry_var = tk.StringVar()
            entry = ttk.Entry(display_frame, width=50, textvariable=entry_var)
            entry.grid(row=i, column=1, sticky=tk.E, padx=5, pady=5)
            self.column_inputs.append(entry_var)

        # submit button
        submit_button = ttk.Button(display_frame, text="Submit", command=self._submit)
        submit_button.grid(row=len(column_names), column=0, columnspan=2)

    def _submit(self):
        """
            The _submit function is called when the user clicks the submit button.

            :param self: Represent the instance of the class
            :return: Nothing
        """
        # get the column names
        column_names = []

        # remove the auto increment column if True
        for column in self._db.get_table_columns(str(self.table_name)):
            if "autoincrement" in column and column["autoincrement"] is False:
                column_names.append(column["name"])
            elif "autoincrement" not in column:
                column_names.append(column["name"])

        column_names = tuple(column_names)

        # get the values from the entry boxes
        values = []
        for i in range(len(column_names)):
            values.append(self.column_inputs[i].get())

        # check the length of the column names and fix the syntax
        if len(column_names) == 1:
            column_names = str(column_names).replace(",", "")
        # replace ' in column name tuple
        column_names = str(column_names).replace("'", "")

        values = tuple(values)
        print("v0: ", values)
        # check the length of the values and fix the syntax
        if len(values) == 1:
            values = str(values).replace(",", "")
            print("v1: ", values)

        print("v len: ", len(values))
        print(values)
        # insert the row
        self.controller.controller.insert_to_table(self.table_name, column_names, values)
        # close the window
        self.dispose()
