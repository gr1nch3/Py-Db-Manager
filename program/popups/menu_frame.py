""" _Summary_ : This file contains the class MenuFrame, which is a frame that
                contains the menu for the program. It is a popup frame that
                is called from the base.py file. It contains the following
                buttons:
                    - edit
                    - delete
"""

# import necessary modules
import tkinter as tk


class MenuFrame(tk.Menu):
    """_summary_: frame for the menu that pops up when a table is right-clicked
    """

    def __init__(self, parent, **kwargs):
        """
            The __init__ function is called when the class is being initiated.

            :param self: Represent the instance of the class
            :param parent: Pass the controller to the menu
            :return: Nothing
        """
        tk.Menu.__init__(self, parent, tearoff=0)
        # controller
        self.controller = parent
        # key word arguments
        self.db_name = kwargs["db_name"] if "db_name" in kwargs else None
        self.table_name = kwargs["table_name"] if "table_name" in kwargs else None
        self.row_value = kwargs["row_value"] if "row_value" in kwargs else None
        self.row_table = kwargs["row_table"] if "row_table" in kwargs else None
        self.hide_alter = kwargs["hide_alter"] if "hide_alter" in kwargs else False

        # close menu when clicked outside
        self.bind("<FocusOut>", lambda event: self.destroy())
        self.add_command(label="Edit", command=self._edit) if not self.hide_alter else None
        self.add_separator()
        self.add_command(label="Delete", command=self._delete)

    # delete database command
    def _delete(self):
        """
            The delete function is called when the user clicks the delete button.
            It removes all references to this object, so that it can be garbage collected.

            :param self: Represent the instance of the class
            :return: The menu
        """
        if self.db_name is not None:
            self.controller.controller.delete_database(self.db_name)
        if self.table_name is not None:
            self.controller.controller.delete_table(self.table_name)
        if self.row_value is not None and self.row_table is not None:
            self.controller.controller.delete_from_table(table_name=self.row_table, condition=self.row_value)
            pass

    # edit database command
    def _edit(self):
        """
            The edit function is called when the user clicks the edit button.
            It removes all references to this object, so that it can be garbage collected.

            :param self: Represent the instance of the class
            :return: The menu
        """
        if self.db_name is not None:
            self.controller.alter_database_frame(event=None, db_name=self.db_name)
        if self.table_name is not None:
            self.controller.alter_table_frame(event=None, table_name=self.table_name)
        if self.row_value is not None and self.row_table is not None:
            self.controller.edit_row(event=None, table_name=self.row_table, row_value=self.row_value)
