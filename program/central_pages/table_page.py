"""_summary_ : Display details about a table and use functions to perform operations
                on the table
"""
# Import the necessary modules
import tkinter as tk
import tkinter.ttk as ttk

# import the necessary classes
from program.popups.menu_frame import MenuFrame
from program.error_handler import ErrorHandler


# noinspection PyUnusedLocal
class TablePage(tk.Frame):
    """_summary_ : Display details about a table and use functions to perform operations
                    on the table
    """

    def __init__(self, parent, table_name: str = None):
        """
            The __init__ function is called when the class is instantiated.
            It sets up the instance of the class, and defines all variables that will be used
            by other functions in the class.


            :param self: Represent the instance of the class
            :param parent: Pass the controller to the class, so that it can be used in other functions
            :param table_name: str: Set the table name
            :return: None
        """
        tk.Frame.__init__(self, parent, width=500, padx=5, pady=5)
        # controller
        self.controller = parent
        self.tablename = table_name if table_name is not None else "None"
        self.label = tk.Label(self, text=f'Table: {table_name}', font=("Arial", 30), bg="grey", justify="center")
        self.label.place(y=0, relx=0.5, relwidth=0.98, anchor="n")

        # Table info
        self.table_info()

        # extra frame(for refresh purposes)
        self.extra_frame = None

        # top frame
        self._top_frame()

        # Table View
        self._view()

    def table_info(self):
        """
            The table_info function is used to display the table name, engine and collation of a selected table.
            The function takes in self as an argument.
            It then creates a frame for the information to be displayed in and places it on top of the grid.
            Next, it displays the name of the selected table using a label widget with font size 15 Arial font type.
            If there is no database connected, nothing will be displayed except for 'Table Name:'.
            If there is one connected however,
            the function will get all tables from that database using get_table_metadata()
            method from Database class which returns all tables

            :param self: Represent the instance of the class
            :return: The name of the table, its engine and collation
        """
        _db = self.controller.controller.current_database
        # grid
        table_info_frame = tk.Frame(self, padx=5, pady=5)
        table_info_frame.place(y=60, height=50, bordermode="outside", relx=0.5, anchor="n", relwidth=0.98)
        # table name
        table_name_label = tk.Label(table_info_frame, text=f'Table name: {self.tablename}',
                                    font=("Arial", 15))
        table_name_label.pack(side="left", padx=5, pady=5)

        if _db is not None:
            _db.connect()
            # get all tables
            td = _db.get_table_metadata()
            # get table data
            table_data = td[self.tablename]
            # get table engine
            table_engine = table_data['engine']
            # get table collation
            table_collation = table_data['collation']

            # table engine
            table_engine_label = tk.Label(table_info_frame, font=("Arial", 15), text=f'Table engine: {table_engine}')
            table_engine_label.pack(side="left", padx=5, pady=5)

            # table collation
            table_collation_label = tk.Label(table_info_frame, text=f'Table collation: {table_collation}',
                                             font=("Arial", 15))
            table_collation_label.pack(side="left", padx=5, pady=5)

    # button frame and grid
    def _top_frame(self):
        """
            The _top_frame function creates the top frame of the table_frame.
            It contains buttons for altering, inserting, deleting and editing a table.
            It also has an entry box to display query strings.

            :param self: Represent the instance of the object that is using this method
            :return: A tuple of the following:
        """
        top_frame = tk.Frame(self, padx=5, pady=5)
        top_frame.place(y=100, height=100, bordermode="outside", relx=0.5, rely=0.01, anchor="n", relwidth=0.98)
        button_frame = tk.Frame(top_frame, padx=5, pady=5)
        button_frame.place(y=0, height=50, bordermode="outside", relx=0.5, anchor="n", relwidth=0.98)

        # button for alter table
        alter_table_button = tk.Button(button_frame, text="Alter Table")
        alter_table_button.pack(side="left", padx=5, pady=5)
        alter_table_button.bind("<Button-1>", lambda e: self.controller.alter_table_frame(event=e,
                                                                                          table_name=self.tablename))

        # button for insert
        insert_button = tk.Button(button_frame, text="insert")
        insert_button.pack(side="left", padx=5, pady=5)
        insert_button.bind("<Button-1>", lambda e: self.controller.insert_frame(event=e, table_name=self.tablename))

        # entry box displaying query string
        self.query_frame = tk.Frame(top_frame, padx=5, pady=5)
        self.query_frame.place(y=100, height=60, bordermode="outside", anchor="s", relx=0.5, relwidth=0.98)

    def _view(self):
        """
            The _view function is responsible for creating the view of the page.
            It creates a frame and places it on the page, then populates that frame with widgets.
            The function also binds events to those widgets.

            :param self: Represent the instance of the class
            :return: A table_tree object
        """
        # database
        _db = self.controller.controller.current_database
        # run query
        # query entry box label
        query_label = tk.Label(self.query_frame, text="Query:")
        query_label.pack(side="left", padx=5, pady=5)
        # query entry box
        # TODO: use query to display data, it only takes SELECT query
        query_var = tk.StringVar()
        query_entry = tk.Entry(self.query_frame, width=100, font=("Arial", 15), textvariable=query_var)
        query_entry.pack(side="left", padx=5, pady=5)
        query_var.set(f"SELECT * FROM {self.tablename} LIMIT 10")
        # query button
        query_button = tk.Button(self.query_frame, text="Submit")
        query_button.pack(side="left", padx=5, pady=5)
        query_button.bind("<Button-1>", lambda e: r_query(e))
        # bind enter key to query button
        query_entry.bind("<Return>", lambda e: r_query(e))

        # table view: treeview
        self.extra_frame = tk.Frame(self, padx=5, pady=5, bg="white")
        self.extra_frame.place(y=240, height=500, bordermode="outside", relx=0.5, anchor="n", relwidth=0.98)

        # table_tree
        table_tree = ttk.Treeview(self.extra_frame, columns=())
        table_tree.pack(fill="both", expand=True)

        # scrollbars
        yscrollbar = ttk.Scrollbar(self.extra_frame, orient="vertical", command=table_tree.yview)
        yscrollbar.pack(side="right", fill="y")
        xscrollbar = ttk.Scrollbar(self.extra_frame, orient="horizontal", command=table_tree.xview)
        xscrollbar.pack(side="bottom", fill="x")
        table_tree.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        def build_tree(data):
            # delete from the tree
            table_tree.delete(*table_tree.get_children())
            _columns = _db.get_table_columns(str(self.tablename))
            # get only the column names
            _columns = tuple([col["name"] for col in _columns])
            table_tree['columns'] = _columns
            # format columns
            table_tree.column("#0", width=0, stretch=False)
            for col in _columns:
                table_tree.column(col, anchor="w", width=100)
                table_tree.heading(col, text=col, anchor="w")

            for i, row in enumerate(data):
                # get the value from the row tuple
                row = list(row)
                # insert the row
                table_tree.insert(parent='', index='end', iid=str(i), text="", values=row)

            # menu popup
            table_tree.bind(
                "<Button-3>",
                lambda e: open_menu_frame(e))

            # table_tree.bind("<Button-3>", lambda e: self.controller.controller.open_menu_frame(e, tv=table_tree))
            def open_menu_frame(event):
                """
                    The open_menu_frame function is called when the user right-clicks on a treeview item.
                    It opens a popup menu that allows the user to delete or edit an item.

                    :param event: Identify the event that caused the function to be called
                    :return: A menu frame object
                """
                # identify the treeview item that was clicked
                item = table_tree.identify_row(event.y)
                # trigger treeview focus
                table_row = str(table_tree.item(item)["values"])
                # map column names to values
                table_row = table_row.replace("[", "").replace("]", "").replace("'", "").split(", ")
                table_row = dict(zip(_columns, table_row))
                # get the column name and value from the dictionary and use it to make a query string
                table_row = [f'{k}="{v}"' for k, v in table_row.items()]
                # make query string
                table_row = str(table_row).replace("[", "").replace("]", "").replace("'", "").replace(",", " AND")
                menu_frame = None

                if item:
                    # activate the top level window
                    try:
                        menu_frame = MenuFrame(self.controller, row_table=self.tablename, row_value=table_row)
                        menu_frame.tk_popup(event.x_root, event.y_root)
                        # get focus
                        menu_frame.focus_set()
                    finally:
                        menu_frame.grab_release()

        # get table data
        if _db is not None:
            _db.connect()
            _data = _db.get_table_data(str(self.tablename))
            build_tree(_data)

        def r_query(event):
            """
                The query function is used to display the query string in the entry box.
                It takes in event as an argument.
                It then gets the query string from the entry box and displays it in the entry box.

                :param event: The event that is passed in
                :return: None
            """
            query_string = query_var.get()
            _db.connect()
            try:
                result = _db.query(query_string)
                _db.disconnect()
                build_tree(result)
            except Exception as e:
                ErrorHandler(self, str(e))
