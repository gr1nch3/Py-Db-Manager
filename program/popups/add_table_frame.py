""" _Summary_ : This file contains the class AddTableFrame, which is a frame
                that pops up when the user wants to add a table. It contains
                the following
                - table name
                - entry box for the user to enter the new table name
                - a button for submitting the changes
"""

# import necessary modules
import tkinter as tk
import tkinter.ttk as ttk


class AddTable(tk.Toplevel):
    """_summary_: frame for adding a table
    """

    def __init__(self, parent, database_name: str):
        """
            The __init__ function is called when the class is being initiated.

            :param self: Represent the instance of the class
            :param parent: Pass the controller to add table frame
            :param database_name: Pass the database name to  add table frame
            :return: Nothing
        """
        tk.Toplevel.__init__(self, parent)
        # controller
        self.controller = parent
        # resizable false
        self.resizable(False, False)
        # self.overrideredirect(True)
        self.transient(parent)
        # close menu when clicked outside
        # change close button function
        self.protocol("WM_DELETE_WINDOW", self.dispose)
        # database name
        self.database_name = database_name
        # title
        self.title("Add Table")
        # current database
        self.cdb = self.controller.controller.current_database
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

    # view function with grid, the grid can be refreshed for the amount of columns and rows added
    def _view(self):
        """
            The _view function is called when the class is being initiated.
            It contains the following
            - table name
            - entry box for the user to enter the new table name

            :param self:
            :return: Nothing
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

        self.columns_length = 1
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
                         "Auto Increment", "Default Value"]
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
                        row_list.append(column_name_var)

                    elif hdr == "Data Type":
                        data_type_var = tk.StringVar()
                        combobox = ttk.Combobox(table_frame, width=10, textvariable=data_type_var)
                        combobox["values"] = data_types
                        combobox.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            data_type_var.set(self.columns_details[i][1].get())
                        row_list.append(data_type_var)

                    elif hdr == "Length":
                        length_var = tk.StringVar()
                        entry = ttk.Entry(table_frame, width=10, textvariable=length_var)
                        entry.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            length_var.set(self.columns_details[i][2].get())
                        row_list.append(length_var)

                    elif hdr == "Primary Key":
                        primary_key_var = tk.IntVar()
                        checkbutton = ttk.Checkbutton(table_frame, onvalue=1, offvalue=0, width=1,
                                                      variable=primary_key_var)
                        checkbutton.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            primary_key_var.set(self.columns_details[i][3].get())
                        row_list.append(primary_key_var)

                    elif hdr == "Not Null":
                        not_null = tk.IntVar()
                        checkbutton = ttk.Checkbutton(table_frame, onvalue=1, offvalue=0, width=1, variable=not_null)
                        checkbutton.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            not_null.set(self.columns_details[i][4].get())
                        row_list.append(not_null)

                    elif hdr == "Unique":
                        unique = tk.IntVar()
                        checkbutton = ttk.Checkbutton(table_frame, onvalue=1, offvalue=0, width=1, variable=unique)
                        checkbutton.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            unique.set(self.columns_details[i][5].get())
                        row_list.append(unique)

                    elif hdr == "Foreign Key":
                        foreign_key_var = tk.StringVar()
                        combobox = ttk.Combobox(table_frame, width=12, textvariable=foreign_key_var)
                        combobox["values"] = table_names
                        combobox.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            foreign_key_var.set(self.columns_details[i][6].get())
                        row_list.append(foreign_key_var)

                    elif hdr == "On Delete":
                        on_delete_var = tk.StringVar()
                        combobox = ttk.Combobox(table_frame, width=12, textvariable=on_delete_var)
                        combobox["values"] = on_delete_options
                        combobox.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            on_delete_var.set(self.columns_details[i][7].get())
                        row_list.append(on_delete_var)

                    elif hdr == "On Update":
                        on_update_var = tk.StringVar()
                        combobox = ttk.Combobox(table_frame, width=12, textvariable=on_update_var)
                        combobox["values"] = on_update_options
                        combobox.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            on_update_var.set(self.columns_details[i][8].get())
                        row_list.append(on_update_var)

                    elif hdr == "Auto Increment":
                        # display checkbutton and entry box for auto increment value
                        auto_increment_check_var = tk.IntVar()
                        checkbutton = ttk.Checkbutton(table_frame, onvalue=1, offvalue=0, width=1,
                                                      variable=auto_increment_check_var)
                        checkbutton.grid(row=2 + i, column=j, sticky="w", padx=2, pady=5)
                        if self.columns_details and i in self.columns_details:
                            auto_increment_check_var.set(self.columns_details[i][9].get())
                        row_list.append(auto_increment_check_var)

                    elif hdr == "Default Value":
                        default_value_var = tk.StringVar()
                        entry = ttk.Entry(table_frame, width=20, textvariable=default_value_var)
                        entry.grid(row=2 + i, column=j, sticky="w", padx=5, pady=5)
                        if self.columns_details and i in self.columns_details:
                            default_value_var.set(self.columns_details[i][10].get())
                        row_list.append(default_value_var)

                self.columns_details[i] = row_list

        # add column function
        def add_column():
            # increase column count by 1
            self.columns_length += 1
            build()

        # # remove column function
        # def remove_column():
        #     # decrease column count by 1
        #     self.columns_length -= 1
        #     # remove the last row from the columns_details
        #     self.columns_details.popitem()
        #     build()

        def submit():
            # get data from the column_details
            # create a tuple for each column
            # return as string

            for_query = {}
            tbl_name = table_name_var.get()

            if tbl_name is not None and tbl_name != "":

                for i in range(self.columns_length):
                    # row_list = []
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
                    column = self.columns_details[i][0].get()
                    if column is not None and column != "":
                        # column name
                        row_dict["column_name"] = column

                        # data type
                        data_type = self.columns_details[i][1].get()
                        if data_type is not None and data_type != "":
                            row_dict["data_type"] = data_type

                        # auto increment
                        auto_increment = self.columns_details[i][9].get()
                        if auto_increment is not None and auto_increment != 0:
                            row_dict["auto_increment"] = auto_increment

                        # length
                        length = self.columns_details[i][2].get()
                        if length is not None and length != "":
                            row_dict["length"] = length

                        # primary key
                        primary_key = self.columns_details[i][3].get()
                        if primary_key is not None and primary_key != 0:
                            row_dict["primary_key"] = primary_key

                        # not null
                        not_null = self.columns_details[i][4].get()
                        if not_null is not None and not_null != 0:
                            if auto_increment is None or auto_increment == 0:
                                row_dict["not_null"] = not_null

                        # unique
                        unique = self.columns_details[i][5].get()
                        if unique is not None and unique != 0:
                            row_dict["unique"] = unique

                        # foreign key
                        foreign_key = self.columns_details[i][6].get()
                        if foreign_key is not None and foreign_key != "":
                            table_name = str(foreign_key).split(" ")[0]
                            column_name_2 = str(foreign_key).split(" ")[1]
                            row_dict["foreign_key"] = [table_name, column_name_2]

                        # on delete
                        on_delete = self.columns_details[i][7].get()
                        if on_delete is not None and on_delete != "":
                            row_dict["on_delete"] = on_delete

                        # on update
                        on_update = self.columns_details[i][8].get()
                        if on_update is not None and on_update != "":
                            row_dict["on_update"] = on_update

                        # default value
                        default_value = self.columns_details[i][10].get()
                        if default_value is not None and default_value != "":
                            row_dict["default_value"] = default_value

                        for_query[i] = row_dict

                # create the query based on the database type
                query_tuple = ()
                foreign_key_string = ""
                primary_key_string = ""
                unique_string = ""
                for i in range(len(for_query)):
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
                                                  f"{for_query[i]['foreign_key'][0]}({for_query[i]['foreign_key'][1]})"
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

                # create the table
                self.controller.controller.add_table(tbl_name, str(query_tuple).replace("'", ""), self.cdb)

            self.dispose()

        # submit button
        # is placed in the button frame on the right side
        submit_button = ttk.Button(button_frame, text="Submit", width=10, command=submit)
        submit_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # add column button
        # is placed in the button frame on the right side
        add_column_button = ttk.Button(button_frame, text="Add Column", width=10, command=add_column)
        add_column_button.pack(side=tk.RIGHT, padx=5, pady=5)

        if self.columns_length > 0:
            build()
