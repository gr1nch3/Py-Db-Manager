""" _Summary_ : This file contains the class EditFrame, which is a frame
                that pops up when the user wants to edit a row. It contains
                the following
                - column names
                - entry boxes for the user to enter the new column values
                - a button for submitting the changes

"""

# import necessary modules
import tkinter as tk
import tkinter.ttk as ttk


class EditFrame(tk.Toplevel):
    """_summary_: frame for inserting a row
    """

    def __init__(self, parent, table_name, row_value):
        """
            The __init__ function is called when the class is being initiated.

            :param self: Represent the instance of the class
            :param parent: Pass the controller to insert frame
            :param row_value: Pass the row data for editing
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
        # row value
        self.row_value = row_value
        # title
        self.title("Alter Row")
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
        # self._db.connect()

        # display the column names vertically in a grid and the entry boxes to the right
        display_frame = tk.Frame(self)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # get the column names from the row value
        new_row = self.row_value.replace(" AND ", ",")
        column_names = []
        column_names_dict = {}

        for column in new_row.split(","):
            column = column.split("=")
            column_names_dict[column[0].strip()] = column[1].replace('"', '').strip()

        # remove the auto increment column if True
        for column in self._db.get_table_columns(str(self.table_name)):
            if "autoincrement" in column and column["autoincrement"] is False:
                column_names.append(column)
            elif "autoincrement" not in column:
                column_names.append(column["name"])

        column_names = tuple(column_names)

        self.column_inputs = []

        # check if the column name is in the column_names_dict
        # if it is, then set the entry box to the value
        # else, set the entry box to empty

        # create a label for each column name
        for i in range(len(column_names)):
            # label
            label = ttk.Label(display_frame, text=column_names[i])
            label.grid(row=i, column=0, sticky=tk.W)
            # entry box
            entry_var = tk.StringVar()
            entry = ttk.Entry(display_frame, width=50, textvariable=entry_var)
            entry.grid(row=i, column=1, sticky=tk.E, padx=5, pady=5)
            if column_names[i] in column_names_dict:
                entry_var.set(column_names_dict[column_names[i]])

            self.column_inputs.append(entry_var)

        # submit button
        submit_button = ttk.Button(display_frame, text="Submit", command=lambda: submit())
        submit_button.grid(row=len(column_names), column=0, columnspan=2)

        def submit():
            # get the values from the entry boxes
            values = []
            for entry_box in self.column_inputs:
                values.append(entry_box.get())

            # check if the values are empty or changed from the one in the column_names_dict
            # if it is, then update the row
            # else, do nothing
            for v in range(len(values)):
                if values[v] != column_names_dict[column_names[v]]:
                    # create a dictionary for the column names and values
                    changing = f'{column_names[v]} = "{values[v]}"'
                    self.controller.controller.update_table_row(self.table_name, changing, self.row_value)
                    break

            # close the window
            self.dispose()
