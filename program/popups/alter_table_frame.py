""" _Summary_ : This file contains the class AlterTableFrame, which is a frame
                that pops up when the user wants to alter a table. It contains
                the following
                - columns names and types
                - entry boxes for the user to enter the new column names and types
                - entry box for default values
                - buttons for adding and removing columns
                - a button for null/not null
                - a button and field for auto increment
                - a button for submitting the changes
"""

# import necessary modules
import tkinter as tk
import tkinter.ttk as ttk

# import necessary classes
from program.error_handler import ErrorHandler


# TODO: Add a refresh for the table view instead of refreshing the whole program
class AlterTable(tk.Toplevel):
    """_summary_: frame for altering a table
    """

    def __init__(self, parent, table_name: str):
        """
            The __init__ function is called when the class is being initiated.

            :param self: Represent the instance of the class
            :param parent: Pass the controller to alter table frame
            :param table_name: Pass the table name to  alter table frame
            :return: Nothing
        """
        tk.Toplevel.__init__(self, parent)
        # controller
        self.controller = parent
        # resizable false
        self.resizable(False, False)
        # self.overrideredirect(True)
        self.transient(parent)
        # current database
        self.cdb = self.controller.controller.current_database
        # change close button function
        self.protocol("WM_DELETE_WINDOW", self.dispose)
        # table name
        self.table_name = table_name
        # title
        self.title("Alter Table")
        # view
        self._view()

    def dispose(self):
        """_summary_ : dispose of the toplevel
                        and clear all fields
        """
        # dispose of the toplevel
        self.destroy()

    def _view(self):
        """
            The _view function is called when the class is being initiated.

            :param self: Represent the instance of the class
        """
        # frames for the view
        # the frames are packed vertically, in order: table name, table, button
        # the width of the frames are the same as the toplevel
        view_frame = tk.Frame(self)
        view_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # table name frame
        table_name_frame = tk.Frame(view_frame)
        table_name_frame.pack(fill=tk.X, expand=True)
        # table frame
        table_frame = tk.Frame(view_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        # button frame
        button_frame = tk.Frame(view_frame)
        button_frame.pack(fill=tk.X, expand=True)

        # get clmns
        columns = self.cdb.get_table_columns(self.table_name)

        # get clmns details
        self.columns_length = len(columns)

        self.columns_details = {}

        # table name
        table_name_var = tk.StringVar()
        table_name_label = ttk.Label(table_name_frame, text="Table Name: ")
        table_name_label.grid(row=0, column=0, sticky="w", pady=10)
        table_name_entry = ttk.Entry(table_name_frame, width=20, textvariable=table_name_var)
        table_name_entry.grid(row=0, column=1, sticky="w", pady=10)

        # grid columns: column name, data type, primary key, not null, unique, default value
        # grid rows: entry, entry, checkbutton, checkbutton, checkbutton, entry

        # grid: columns
        # Create header labels
        header_labels = ["Column Name", "Data Type", "Length",
                         "Primary Key", "Not Null", "Unique",
                         "Foreign Key", "On Delete", "On Update",
                         "Auto Increment", "Default Value"]  # remove header

        for col, header in enumerate(header_labels):
            label = tk.Label(table_frame, text=header, padx=10, pady=5)
            label.grid(row=1, column=col, sticky="w", padx=5, pady=5)

        # data types
        if self.cdb.db_type == "mssql":
            data_types = ["BIT", "TINYINT", "SMALLINT", "INT", "BIGINT", "FLOAT", "REAL", "DECIMAL", "NUMERIC", "CHAR",
                          "VARCHAR", "NCHAR", "NVARCHAR", "TEXT", "DATE", "TIME", "DATETIME", "TIMESTAMP"]
        elif self.cdb.db_type == "postgresql":
            data_types = ["SMALLINT", "INTEGER", "BIGINT", "DECIMAL", "NUMERIC", "REAL", "DOUBLE PRECISION", "CHAR",
                          "VARCHAR", "TEXT", "DATE", "TIME", "TIMESTAMP", "BOOLEAN"]
        elif self.cdb.db_type == "mysql":
            data_types = ["BIT", "TINYINT", "SMALLINT", "INT", "BIGINT", "FLOAT", "DOUBLE", "DECIMAL", "CHAR",
                          "VARCHAR", "BINARY", "VARBINARY", "TINYBLOB", "BLOB", "MEDIUMBLOB", "LONGBLOB", "TINYTEXT",
                          "TEXT", "MEDIUMTEXT", "LONGTEXT", "DATE", "TIME", "DATETIME", "TIMESTAMP", "ENUM", "SET"]
        else:
            data_types = []

        # table names for ForeignKey combobox
        table_names = []
        tables = self.cdb.get_tables()
        for table in tables:
            tbl_col = self.cdb.get_table_columns(table)
            if tbl_col:
                # list comprehension
                table_names += [f"{table} {tbl['name']}" for tbl in tbl_col]

        # on delete options
        on_delete_options = ["NO ACTION", "CASCADE", "SET NULL", "SET DEFAULT"]
        # on update options
        on_update_options = ["NO ACTION", "CASCADE", "SET NULL", "SET DEFAULT"]

        # grid: rows
        # use a for loop for the amount of columns added
        def build():
            print("columns: ", columns)
            # set the table name
            table_name_var.set(str(self.table_name))
            # using list instead of dictionary
            for i in range(self.columns_length):
                row_list = []
                for j, hdr in enumerate(header_labels):
                    if hdr == "Column Name":
                        column_name_var = tk.StringVar()
                        entry = ttk.Entry(table_frame, width=20, textvariable=column_name_var)
                        entry.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            column_name_var.set(self.columns_details[i][0].get())
                        elif len(columns) > i and "name" in columns[i].keys():
                            column_name_var.set(columns[i].get("name"))
                        row_list.append(column_name_var)

                    elif hdr == "Data Type":
                        data_type_var = tk.StringVar()
                        combobox = ttk.Combobox(table_frame, width=10, textvariable=data_type_var)
                        combobox["values"] = data_types
                        combobox.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            data_type_var.set(self.columns_details[i][1].get())
                        elif len(columns) > i and "type" in columns[i].keys():
                            data_type_var.set(str(columns[i].get("type")).split("(")[0])

                        row_list.append(data_type_var)

                    elif hdr == "Length":
                        length_var = tk.StringVar()
                        entry = ttk.Entry(table_frame, width=10, textvariable=length_var)
                        entry.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            length_var.set(self.columns_details[i][2].get())
                        elif len(columns) > i and "type" in columns[i].keys():
                            data_type = columns[i].get("type")
                            # Extracting the length from the data type value
                            length = ""
                            if str(data_type).__contains__("(") and str(data_type).__contains__(")"):
                                # get the value between the brackets
                                length = str(data_type).split("(")[1].split(")")[0]

                            length_var.set(length)

                        row_list.append(length_var)

                    elif hdr == "Primary Key":
                        primary_key_var = tk.IntVar()
                        checkbutton = ttk.Checkbutton(table_frame, onvalue=1, offvalue=0, width=1,
                                                      variable=primary_key_var)
                        checkbutton.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            primary_key_var.set(self.columns_details[i][3].get())
                        elif len(columns) > i and "primary_key" in columns[i].keys():
                            if columns[i].get("primary_key") is False:
                                primary_key_var.set(0)
                            else:
                                primary_key_var.set(1)

                        row_list.append(primary_key_var)

                    elif hdr == "Not Null":
                        not_null = tk.IntVar()
                        checkbutton = ttk.Checkbutton(table_frame, onvalue=1, offvalue=0, width=1, variable=not_null)
                        checkbutton.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            not_null.set(self.columns_details[i][4].get())
                        elif len(columns) > i and "nullable" in columns[i].keys():
                            if columns[i].get("nullable") is False:
                                not_null.set(1)
                            else:
                                not_null.set(0)

                        row_list.append(not_null)

                    elif hdr == "Unique":
                        unique = tk.IntVar()
                        checkbutton = ttk.Checkbutton(table_frame, onvalue=1, offvalue=0, width=1, variable=unique)
                        checkbutton.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            unique.set(self.columns_details[i][5].get())
                        elif len(columns) > i and "unique" in columns[i].keys():
                            if columns[i].get("unique") is False:
                                unique.set(0)
                            else:
                                unique.set(1)

                        row_list.append(unique)

                    elif hdr == "Foreign Key":
                        foreign_key_var = tk.StringVar()
                        combobox = ttk.Combobox(table_frame, width=12, textvariable=foreign_key_var)
                        combobox["values"] = table_names
                        combobox.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            foreign_key_var.set(self.columns_details[i][6].get())
                        elif len(columns) > i and "foreign_key" in columns[i].keys():
                            foreign_key_var.set(columns[i].get("foreign_key"))

                        row_list.append(foreign_key_var)

                    elif hdr == "On Delete":
                        on_delete_var = tk.StringVar()
                        combobox = ttk.Combobox(table_frame, width=12, textvariable=on_delete_var)
                        combobox["values"] = on_delete_options
                        combobox.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            on_delete_var.set(self.columns_details[i][7].get())
                        elif len(columns) > i and "ondelete" in columns[i].keys():
                            on_delete_var.set(columns[i].get("ondelete"))

                        row_list.append(on_delete_var)

                    elif hdr == "On Update":
                        on_update_var = tk.StringVar()
                        combobox = ttk.Combobox(table_frame, width=12, textvariable=on_update_var)
                        combobox["values"] = on_update_options
                        combobox.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            on_update_var.set(self.columns_details[i][8].get())
                        elif len(columns) > i and "onupdate" in columns[i].keys():
                            on_update_var.set(columns[i].get("onupdate"))
                        else:
                            on_update_var.set("")

                        row_list.append(on_update_var)

                    elif hdr == "Auto Increment":
                        # display checkbutton and entry box for auto increment value
                        auto_increment_check_var = tk.IntVar()
                        checkbutton = ttk.Checkbutton(table_frame, onvalue=1, offvalue=0, width=1,
                                                      variable=auto_increment_check_var)
                        checkbutton.grid(row=2 + i, column=j, sticky="w", padx=2, pady=5)
                        if self.columns_details and i in self.columns_details:
                            auto_increment_check_var.set(self.columns_details[i][9].get())
                        elif len(columns) > i and "autoincrement" in columns[i].keys():
                            if columns[i].get("autoincrement") is False:
                                auto_increment_check_var.set(0)
                            else:
                                auto_increment_check_var.set(1)

                        row_list.append(auto_increment_check_var)

                    elif hdr == "Default Value":
                        default_value_var = tk.StringVar()
                        entry = ttk.Entry(table_frame, width=20, textvariable=default_value_var)
                        entry.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            default_value_var.set(self.columns_details[i][10].get())
                        elif len(columns) > i and "default" in columns[i].keys():
                            if columns[i].get("default") is None:
                                default_value_var.set("")
                            else:
                                default_value_var.set(columns[i].get("default"))

                        row_list.append(default_value_var)

                    # remove button
                    # elif hdr == "Remove":
                    #     remove_button = ttk.Button(table_frame, text="Remove", width=10, command=remove_column)
                    #     remove_button.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                    else:
                        print(f"Unknown header: {hdr}")
                self.columns_details[i] = row_list

        # add column function
        def add_column():
            # increase column count by 1
            self.columns_length += 1
            build()

        # build the table
        # MONSTROSITY!!!
        def submit():
            # get data from the column_details
            # create a tuple for each column
            # return as string

            for_query = {}
            tbl_name = table_name_var.get()

            # check if table name is empty or changed
            if tbl_name is not None or tbl_name != "":
                if tbl_name != self.table_name:
                    try:
                        query = ""
                        # run query to rename table
                        if self.cdb.db_type == "mysql":
                            query += f"RENAME TABLE {self.table_name} TO {tbl_name};"
                        elif self.cdb.db_type == "postgresql":
                            query += f"ALTER TABLE {self.table_name} RENAME TO {tbl_name};"
                        elif self.cdb.db_type == "mssql":
                            query += f"EXEC sp_rename '{self.table_name}', '{tbl_name}';"

                        self.cdb.execute_query(query)
                    except Exception as e:
                        ErrorHandler(self.controller.controller, str(e))
                        self.dispose()

                # if the number of columns is different from the number of columns in the database
                # then it means that the user has added or removed a column

                # check if the self.columns_length is greater or less than the length of the columns_details
                max_existing_column_index = len(columns)
                # check for empty column name to avoid errors
                new_dict = dict(filter(lambda elem: elem[1][0].get() != "", self.columns_details.items()))
                new_column_index = len(new_dict)

                # safe check to avoid looping errors
                # noinspection PyUnusedLocal
                loop_start = 0  # set the range the loop will run for
                loop_count = 0  # set the number of times the loop will run

                # pylint: disable=C0206
                # pylint: disable=C0201
                for column_index in self.columns_details.keys(): # noqa
                    column_details = self.columns_details[column_index]
                    new_columns = columns[column_index]  # despite the name, this is the old columns data from the db

                    # if the column_index is greater than the max_existing_column_index
                    # it means that the user has added a column
                    if new_column_index > max_existing_column_index:
                        # get the difference between the column_index and the max_existing_column_index
                        # this will be the number of columns that the user has added
                        difference = new_column_index - max_existing_column_index

                        # get the new columns
                        added_columns = dict(list(self.columns_details.items())[-difference:])
                        # map the new columns to a new dictionary that the key starts from 0
                        added_columns = dict(enumerate(added_columns.values()))

                        # loop through the difference and add it to the for query
                        loop_start = difference
                        if loop_count == loop_start:
                            break
                        else:
                            for i in range(difference):
                                row_dict = {
                                    "column_name": "",
                                    "data_type": "",
                                    "length": "",
                                    "primary_key": "",
                                    "not_null": "",
                                    "unique": "",
                                    "foreign_key": "",
                                    "on_delete": "",
                                    "on_update": "",
                                    "auto_increment": "",
                                    "default_value": ""
                                }
                                # only add column if column name is not empty
                                new_column_name = added_columns[i][0].get()
                                if new_column_name is not None and new_column_name != "":
                                    # column name
                                    row_dict["column_name"] = new_column_name

                                    # data type
                                    new_data_type = added_columns[i][1].get()
                                    if new_data_type is not None and new_data_type != "":
                                        row_dict["data_type"] = new_data_type

                                    # auto increment
                                    new_auto_increment = added_columns[i][9].get()
                                    if new_auto_increment is not None and new_auto_increment != 0:
                                        row_dict["auto_increment"] = new_auto_increment

                                    # length
                                    new_length = added_columns[i][2].get()
                                    if new_length is not None and new_length != "":
                                        row_dict["length"] = new_length

                                    # primary key
                                    new_primary_key = added_columns[i][3].get()
                                    if new_primary_key is not None and new_primary_key != 0:
                                        row_dict["primary_key"] = new_primary_key

                                    # not null
                                    new_not_null = added_columns[i][4].get()
                                    if new_not_null is not None and new_not_null != 0:
                                        if new_auto_increment is None or new_auto_increment == 0:
                                            row_dict["not_null"] = new_not_null

                                    # unique
                                    new_unique = added_columns[i][5].get()
                                    if new_unique is not None and new_unique != 0:
                                        row_dict["unique"] = new_unique

                                    # foreign key
                                    new_foreign_key = added_columns[i][6].get()
                                    if new_foreign_key is not None and new_foreign_key != "":
                                        table_name = str(new_foreign_key).split(" ")[0]
                                        column_name_2 = str(new_foreign_key).split(" ")[1]
                                        row_dict["foreign_key"] = [table_name, column_name_2]

                                    # on delete
                                    new_on_delete = added_columns[i][7].get()
                                    if new_on_delete is not None and new_on_delete != "":
                                        row_dict["on_delete"] = new_on_delete

                                    # on update
                                    new_on_update = added_columns[i][8].get()
                                    if new_on_update is not None and new_on_update != "":
                                        row_dict["on_update"] = new_on_update

                                    # default value
                                    new_default_value = added_columns[i][10].get()
                                    if new_default_value is not None and new_default_value != "":
                                        row_dict["default_value"] = new_default_value

                                    for_query[i] = row_dict
                                    loop_count += 1

                    # if the column_index is less than the max_existing_column_index
                    # it means that the user has removed a column
                    elif new_column_index < max_existing_column_index:
                        # get the difference between the column_index and the max_existing_column_index
                        # this will be the number of columns that the user has removed
                        difference = max_existing_column_index - new_column_index

                        # get the removed columns
                        # the removed item will not be in the columns
                        removed_columns = [i["name"] for i in columns if i["name"] != ""]
                        for i in range(len(removed_columns)):
                            if self.columns_details[i][0].get() in removed_columns:
                                removed_columns.remove(self.columns_details[i][0].get())

                        # loop through the difference and add it to the for query
                        loop_start = difference
                        if loop_count == loop_start:
                            break
                        else:
                            for i in range(difference):
                                # column name
                                column_name = removed_columns[i]

                                # if the column name is not empty
                                if column_name is not None and column_name != "":
                                    query = ""
                                    # drop column
                                    if self.cdb.db_type == "mysql":
                                        query += f" DROP COLUMN {column_name}"
                                    elif self.cdb.db_type == "postgresql":
                                        query += f" DROP COLUMN {column_name}"
                                    elif self.cdb.db_type == "mssql":
                                        query += f"ALTER TABLE {tbl_name} DROP COLUMN {column_name};"
                                    # run the query
                                    self.controller.controller.alter_table(tbl_name, query)
                                loop_count += 1

                    # if the column_index is equal to the max_existing_column_index
                    # it means that the user has not added or removed a column
                    elif new_column_index == max_existing_column_index:

                        #    solution: 1. make sure the columns and self.columns_details are the same
                        #               in order, data type and data order
                        #             2. loop through the columns and self.columns_details and compare
                        #               the values, if any changes are found, run the query

                        #          Note: the column_detalis is a list of tkinter variables

                        # only add column if column name is not empty
                        column = column_details[0].get()
                        if column is not None and column != "":
                            # column name
                            if new_columns["name"] != column:
                                # run query to rename column
                                query = ""
                                if self.cdb.db_type == "mysql":
                                    query = f" CHANGE {new_columns['name']} {column} {new_columns['type']}"
                                elif self.cdb.db_type == "postgresql":
                                    query = f" RENAME COLUMN {new_columns['name']} TO {column}"
                                elif self.cdb.db_type == "mssql":
                                    query = f"EXEC sp_rename '{tbl_name}.{new_columns['name']}', '{column}';"
                                # run the query
                                self.controller.controller.alter_table(tbl_name, query)

                            # data type
                            data_type = column_details[1].get()
                            if data_type is not None and data_type != "":
                                if str(new_columns["type"]).split("(")[0] != data_type:
                                    print("data type has changed")
                                    query = ""
                                    if self.cdb.db_type == "mysql":
                                        query = f" MODIFY {column} {str(data_type).split('(')[0]}"
                                    elif self.cdb.db_type == "postgresql":
                                        query = f" ALTER COLUMN {column} TYPE {str(data_type).split('(')[0]}"
                                    elif self.cdb.db_type == "mssql":
                                        query = f"ALTER TABLE {tbl_name} ALTER COLUMN {column} " \
                                                f"{str(data_type).split('(')[0]};"
                                    # run the query
                                    self.controller.controller.alter_table(tbl_name, query)

                            # auto increment
                            auto_increment = column_details[9].get()
                            if auto_increment is not None and auto_increment != 0:
                                if "autoincrement" in new_columns.keys():
                                    if new_columns["autoincrement"] != bool(auto_increment):
                                        # check if it's adding or removing auto increment
                                        query = ""
                                        if auto_increment == 1:
                                            if self.cdb.db_type == "mysql":
                                                query = f" MODIFY {column} {data_type} AUTO_INCREMENT"
                                            elif self.cdb.db_type == "postgresql":
                                                query = f" ALTER COLUMN {column} TYPE {data_type} AUTO_INCREMENT"
                                            elif self.cdb.db_type == "mssql":
                                                query = f"ALTER TABLE {tbl_name} ALTER COLUMN {column} " \
                                                        f"{data_type} IDENTITY(1,1);"
                                        else:
                                            if self.cdb.db_type == "mysql":
                                                query = f" MODIFY {column} {data_type};"
                                            elif self.cdb.db_type == "postgresql":
                                                query = f" ALTER COLUMN {column} TYPE {data_type};"
                                            elif self.cdb.db_type == "mssql":
                                                query = f"ALTER TABLE {tbl_name} ALTER COLUMN {column} {data_type};"
                                        # run the query
                                        self.controller.controller.alter_table(tbl_name, query)

                            # not null
                            not_null = column_details[4].get()
                            if not_null is not None and not_null != 0:
                                if auto_increment is None or auto_increment == 0:
                                    if "nullable" in new_columns.keys():
                                        # using reverse order because of data structure
                                        # not_null_value = False means a column can't be null
                                        # not_null_value = True means a column can be null
                                        not_null_value = False if not_null == 1 else True
                                        if new_columns["nullable"] != not_null_value:
                                            print(f"nn1: {new_columns['nullable']} | nn2: {not_null_value}")
                                            print("not null has changed")
                                            print()
                                            # check if it's adding or removing not null
                                            # using number instead of boolean because of tkinter
                                            query = ""
                                            if not_null_value is False:
                                                if self.cdb.db_type == "mysql":
                                                    query = f" MODIFY {column} {new_columns['type']} NOT NULL"
                                                elif self.cdb.db_type == "postgresql":
                                                    query = f" ALTER COLUMN {column} SET NOT NULL"
                                                elif self.cdb.db_type == "mssql":
                                                    query = f"ALTER TABLE {tbl_name} ALTER COLUMN {column} NOT NULL;"
                                            else:
                                                if self.cdb.db_type == "mysql":
                                                    query = f" MODIFY {column} {new_columns['type']} NULL"
                                                elif self.cdb.db_type == "postgresql":
                                                    query = f" ALTER COLUMN {column} DROP NOT NULL"
                                                elif self.cdb.db_type == "mssql":
                                                    query = f"ALTER TABLE {tbl_name} ALTER COLUMN {column} NULL;"
                                            # run the query
                                            self.controller.controller.alter_table(tbl_name, query)

                            # length
                            length = column_details[2].get()
                            if length is not None and length != "":
                                data_type = new_columns.get("type")
                                # Extracting the length from the data type value
                                length2 = ""
                                if str(data_type).__contains__("(") and str(data_type).__contains__(")"):
                                    # get the value between the brackets
                                    length2 = str(data_type).split("(")[1].split(")")[0]
                                    if length2.__contains__("="):
                                        length2 = length2.split("=")[1]
                                if length != length2:
                                    print("length has changed")
                                    query = ""
                                    if self.cdb.db_type == "mysql":
                                        query = f" MODIFY {column} {str(data_type).split('(')[0]}({length})"
                                    elif self.cdb.db_type == "postgresql":
                                        query = f" ALTER COLUMN {column} TYPE {str(data_type).split('(')[0]}({length})"
                                    elif self.cdb.db_type == "mssql":
                                        query = f"ALTER TABLE {tbl_name} ALTER COLUMN {column} " \
                                                f"{str(data_type).split('(')[0]}({length});"
                                    # run the query
                                    self.controller.controller.alter_table(tbl_name, query)

                            # primary key
                            primary_key = column_details[3].get()
                            if primary_key is not None and primary_key != 0:
                                if "primary_key" in new_columns.keys():
                                    if new_columns["primary_key"] != bool(primary_key):
                                        print(f"pk1: {new_columns['primary_key']} | pk2: {primary_key}")
                                        # check if it's adding or removing primary key
                                        query = ""
                                        if primary_key == 1:
                                            if self.cdb.db_type == "mysql":
                                                query = f" ADD PRIMARY KEY ({column});"
                                            elif self.cdb.db_type == "postgresql":
                                                query = f" ADD CONSTRAINT pk_{tbl_name} PRIMARY KEY ({column});"
                                            elif self.cdb.db_type == "mssql":
                                                query = f"ALTER TABLE {tbl_name} ADD CONSTRAINT pk_{tbl_name} " \
                                                        f"PRIMARY KEY ({column});"
                                        else:
                                            if self.cdb.db_type == "mysql":
                                                query = f" DROP PRIMARY KEY;"
                                            elif self.cdb.db_type == "postgresql":
                                                query = f" DROP CONSTRAINT pk_{tbl_name};"
                                            elif self.cdb.db_type == "mssql":
                                                query = f"ALTER TABLE {tbl_name} DROP CONSTRAINT pk_{tbl_name};"
                                        # run the query
                                        self.controller.controller.alter_table(tbl_name, query)

                            # unique
                            unique = column_details[5].get()
                            if unique is not None and unique != 0:
                                if "unique" in new_columns.keys():
                                    if new_columns["unique"] != bool(unique):
                                        print(f"u1: {new_columns['unique']} | u2: {unique}")
                                        # check if it's adding or removing unique
                                        query = ""
                                        if unique == 1:
                                            if self.cdb.db_type == "mysql":
                                                query = f" ADD UNIQUE ({column});"
                                            elif self.cdb.db_type == "postgresql":
                                                query = f" ADD CONSTRAINT {tbl_name}_unique UNIQUE ({column});"
                                            elif self.cdb.db_type == "mssql":
                                                query = f"ALTER TABLE {tbl_name} ADD CONSTRAINT " \
                                                        f"{tbl_name}_unique UNIQUE ({column});"
                                        else:
                                            if self.cdb.db_type == "mysql":
                                                query = f" DROP INDEX {column};"
                                            elif self.cdb.db_type == "postgresql":
                                                query = f" DROP CONSTRAINT {tbl_name}_unique;"
                                            elif self.cdb.db_type == "mssql":
                                                query = f"ALTER TABLE {tbl_name} DROP CONSTRAINT {tbl_name}_unique;"
                                        # run the query
                                        self.controller.controller.alter_table(tbl_name, query)

                            # foreign key
                            foreign_key = column_details[6].get()
                            # on delete
                            on_delete = column_details[7].get()
                            # on update
                            on_update = column_details[8].get()
                            if foreign_key is not None and foreign_key != "":
                                table_name = str(foreign_key).split(" ")[0]
                                column_name_2 = str(foreign_key).split(" ")[1]
                                od = ""
                                ou = ""
                                query = ""
                                if "foreign_key" in new_columns.keys():
                                    # handle on delete and on update
                                    if on_delete is not None and on_delete != "":
                                        if "ondelete" in new_columns.keys():
                                            if new_columns["ondelete"] != on_delete:
                                                od = f' ON DELETE {on_delete}'
                                            else:
                                                od = " DEFAULT"
                                    if on_update is not None and on_update != "":
                                        if "onupdate" in new_columns.keys():
                                            if new_columns["onupdate"] != on_update:
                                                ou = f' ON UPDATE {on_update}'
                                            else:
                                                ou = " DEFAULT"
                                    if new_columns["foreign_key"] != f"{table_name} {column_name_2}":
                                        # check if it's adding or removing foreign key
                                        if foreign_key != "":
                                            query = ""
                                            if self.cdb.db_type == "mysql":
                                                query = f" ADD FOREIGN KEY ({column}) REFERENCES {table_name}" \
                                                        f"({column_name_2}) " \
                                                        f"{od} " \
                                                        f"{ou}"
                                            elif self.cdb.db_type == "postgresql":
                                                query = f" ADD CONSTRAINT {table_name} FOREIGN KEY ({column}) " \
                                                        f"REFERENCES " \
                                                        f"{table_name}({column_name_2}" \
                                                        f"{od}" \
                                                        f"{ou})"
                                            elif self.cdb.db_type == "mssql":
                                                query = f"ALTER TABLE {table_name} ADD CONSTRAINT {table_name}" \
                                                        f" FOREIGN KEY " \
                                                        f"({column}) REFERENCES {table_name}({column_name_2}" \
                                                        f"{od}" \
                                                        f"{ou});"
                                        else:
                                            if self.cdb.db_type == "mysql":
                                                query = f" DROP FOREIGN KEY fk_{column}"
                                            elif self.cdb.db_type == "postgresql":
                                                query = f" DROP CONSTRAINT fk_{column}"
                                            elif self.cdb.db_type == "mssql":
                                                query = f"ALTER TABLE {table_name} DROP CONSTRAINT fk_{tbl_name};"
                                        # run the query
                                        self.controller.controller.alter_table(tbl_name, query)

                            # default value
                            default_value = column_details[10].get()
                            if default_value is not None and default_value != "":
                                if "default" in new_columns.keys():
                                    if new_columns["default"] != default_value:
                                        query = ""
                                        if self.cdb.db_type == "mysql":
                                            query = f" ALTER {column} SET DEFAULT {default_value}"
                                        elif self.cdb.db_type == "postgresql":
                                            query = f" ALTER {column} SET DEFAULT {default_value}"
                                        elif self.cdb.db_type == "mssql":
                                            query = f"ALTER TABLE {tbl_name} ALTER COLUMN {column} " \
                                                    f"SET DEFAULT {default_value};"
                                        # run the query
                                        self.controller.controller.alter_table(tbl_name, query)

                # create the query based on the database type
                query_tuple = ()
                foreign_key_string = ""
                primary_key_string = ""
                unique_string = ""
                # adding column to the table
                if len(for_query) > 0:
                    print("for q: \n", for_query)
                    # pylint: disable=C0200
                    for i in range(len(for_query)): # this iworks better than enumerate
                        if self.cdb.db_type == "mysql":
                            query = f"{for_query[i]['column_name']} {for_query[i]['data_type']}"
                            if for_query[i]['length'] != "":
                                query += f"({for_query[i]['length']})"
                            if for_query[i]['primary_key'] != "":
                                primary_key_string += f"PRIMARY KEY ({for_query[i]['column_name']})"
                            if for_query[i]['not_null'] != "":
                                query += " NOT NULL"
                            if for_query[i]['unique'] != "":
                                unique_string += f"UNIQUE ({for_query[i]['column_name']})"
                            if for_query[i]['auto_increment'] != "":
                                query += " AUTO_INCREMENT"
                            if for_query[i]['default_value'] != "":
                                query += f" DEFAULT {for_query[i]['default_value']}"
                            if for_query[i]['foreign_key'] != "":
                                foreign_key_string += f"FOREIGN KEY ({for_query[i]['column_name']}) " \
                                                      f"REFERENCES {for_query[i]['foreign_key'][0]}" \
                                                      f"({for_query[i]['foreign_key'][1]})"
                                if for_query[i]['on_delete'] != "":
                                    foreign_key_string += f" ON DELETE {for_query[i]['on_delete']}"
                                if for_query[i]['on_update'] != "":
                                    foreign_key_string += f" ON UPDATE {for_query[i]['on_update']}"

                            # add primary key and foreign key to the query at the end
                            if i == len(for_query) - 1:
                                if unique_string != "":
                                    query += f", {unique_string}"
                                if primary_key_string != "":
                                    query += f", {primary_key_string}"
                                if foreign_key_string != "":
                                    query += f", {foreign_key_string}"
                            query_tuple += (query,)

                        if self.cdb.db_type == "mssql":
                            query = f"{for_query[i]['column_name']} {for_query[i]['data_type']}"
                            if for_query[i]['length'] != "":
                                query += f"({for_query[i]['length']})"
                            if for_query[i]['primary_key'] != "":
                                query += " PRIMARY KEY"
                            if for_query[i]['not_null'] != "":
                                query += " NOT NULL"
                            if for_query[i]['unique'] != "":
                                query += " UNIQUE"
                            if for_query[i]['auto_increment'] != "":
                                query += " IDENTITY"
                            if for_query[i]['default_value'] != "":
                                query += f" DEFAULT {for_query[i]['default_value']}"
                            if for_query[i]['foreign_key'] != "":
                                query += f" FOREIGN KEY REFERENCES {for_query[i]['foreign_key'][0]}" \
                                         f"({for_query[i]['foreign_key'][1]})"
                                if for_query[i]['on_delete'] != "":
                                    query += f" ON DELETE {for_query[i]['on_delete']}"
                                if for_query[i]['on_update'] != "":
                                    query += f" ON UPDATE {for_query[i]['on_update']}"

                            query_tuple += (query,)

                        if self.cdb.db_type == "postgresql":
                            query = f"{for_query[i]['column_name']} {for_query[i]['data_type']}"
                            if for_query[i]['length'] != "":
                                query += f"({for_query[i]['length']})"
                            if for_query[i]['primary_key'] != "":
                                primary_key_string += f"CONSTRAINT pk_{for_query[i]['column_name']} PRIMARY KEY " \
                                                        f"({for_query[i]['column_name']})"
                            if for_query[i]['not_null'] != "":
                                query += " NOT NULL"
                            if for_query[i]['unique'] != "":
                                unique_string += f"UNIQUE ({for_query[i]['column_name']})"
                            if for_query[i]['auto_increment'] != "":
                                query += " AUTO_INCREMENT"
                            if for_query[i]['default_value'] != "":
                                query += f" DEFAULT {for_query[i]['default_value']}"
                            if for_query[i]['foreign_key'] != "":
                                foreign_key_string += f"CONSTRAINT fk_{for_query[i]['column_name']} FOREIGN KEY " \
                                                      f"({for_query[i]['column_name']}) REFERENCES " \
                                                      f"{for_query[i]['foreign_key'][0]}" \
                                                      f"({for_query[i]['foreign_key'][1]})"
                                if for_query[i]['on_delete'] != "":
                                    foreign_key_string += f" ON DELETE {for_query[i]['on_delete']}"
                                if for_query[i]['on_update'] != "":
                                    foreign_key_string += f" ON UPDATE {for_query[i]['on_update']}"

                            # add primary key and foreign key to the query at the end
                            if i == len(for_query) - 1:
                                if unique_string != "":
                                    query += f", {unique_string}"
                                if primary_key_string != "":
                                    query += f", {primary_key_string}"
                                if foreign_key_string != "":
                                    query += f", {foreign_key_string}"

                            query_tuple += (query,)

                    qt_query = ""
                    # strip the query_tuple from the last comma
                    if len(query_tuple) == 1:
                        qt_query = f"ADD {query_tuple[0]}"
                    else:
                        for q in query_tuple:

                            # last item in the loop
                            if q == query_tuple[-1]:
                                qt_query += f"ADD COLUMN {q}"
                            else:
                                qt_query += f"ADD COLUMN {q}, "

                    query_tuple = qt_query

                    # create the Column
                    self.controller.controller.alter_table(tbl_name, f" {query_tuple}")

            self.dispose()

        # submit button
        # is placed in the button frame on the right side
        submit_button = ttk.Button(button_frame, text="Submit", width=10, command=submit)
        submit_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # add column button
        # is placed in the button frame on the right side
        add_column_button = ttk.Button(button_frame, text="Add Column", width=10, command=add_column)
        add_column_button.pack(side=tk.RIGHT, padx=5, pady=5)
        # add_column_button.bind("<Button-1>", lambda: add_column())

        if self.columns_length > 0:
            build()
