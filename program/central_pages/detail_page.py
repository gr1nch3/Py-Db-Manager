"""_summary_ : Display with functions for database manipulation
"""
# Import the necessary modules
import tkinter as tk
import tkinter.ttk as ttk

# import the necessary classes
from program.popups.menu_frame import MenuFrame
from program.error_handler import ErrorHandler


class DetailPage(tk.Frame):
    """_summary_: main view for the tkinter program that contains a sidebar"""

    def __init__(self, parent):
        """
            The __init__ function is called when the class is instantiated.
            It sets up the instance of the class, and makes sure it has everything it needs to function properly.


            :param self: Represent the instance of the class
            :param parent: Reference the parent class, which is the tk
            :return: A frame
        """
        tk.Frame.__init__(self, parent, width=500, padx=5, pady=5)
        # controller
        self.controller = parent

        # label
        self.label = tk.Label(self, text=f'Database: {self.controller.controller.current_database.db_name}',
                              font=("Arial", 30), bg="grey", justify="left")
        self.label.place(y=0, relx=0.5, relwidth=0.98, anchor="n")

        # extra frame(for refresh purposes)
        self.extra_frame = None

        # button frame
        self._top_frame()
        # view
        self._view()

    # refresh view
    # TODO: create a refresh function for the views or trees
    # def refresh_view(self):
    #     """
    #         The refresh_view function is used to refresh the view of the frame.
    #         It is called when a new table is added or when a table is deleted.
    #         It uses the get_table_details function from controller.py to retrieve all table details
    #         and then displays them in a treeview widget.
    #
    #         :param self: Represent the instance of the object that calls the method
    #         :return: A frame with a treeview that displays the list of tables
    #     """
    #     # destroy the treeview widget
    #     self.extra_frame.destroy()
    #     self.extra_frame = None
    #     # create a new treeview widget
    #     self._view()

    # button frame and grid
    def _top_frame(self):
        """
            The _top_frame function creates the top frame of the main window.
            It contains a button for adding tables, a button for altering databases,
            and an entry field with a search button.


            :param self: Represent the instance of the object itself
            :return: A frame with buttons for adding table and altering database
        """
        top_frame = tk.Frame(self, padx=5, pady=5)
        top_frame.place(y=60, height=50, bordermode="outside", relx=0.5, rely=0.01, anchor="n", relwidth=0.98)
        button_frame = tk.Frame(top_frame, padx=5, pady=5)
        button_frame.place(y=0, height=50, bordermode="outside", relx=0.5, anchor="n", relwidth=0.98)

        # button for adding table
        add_table_button = tk.Button(button_frame, text="Add Table")
        add_table_button.pack(side="left", padx=5, pady=5)
        add_table_button.bind("<Button-1>", lambda e: self.controller.add_table_frame(e))

    # view with details for table or database
    # noinspection PyTypeChecker
    def _view(self):
        """
            The _view function is responsible for creating the widgets that will be displayed on the page.
            It also binds any functions to those widgets that are necessary for their functionality.
            The _view function should not contain any logic, only widget creation and binding.

            :param self: Represent the instance of the object itself
            :return: A frame with a treeview and a grid
        """
        self.extra_frame = tk.Frame(self, height=200, borderwidth=2, relief="groove", padx=5, pady=5, bg="white")
        self.extra_frame.place(y=160, height=200, bordermode="outside", relx=0.5, anchor="n", relwidth=0.98)
        grid_frame = tk.Frame(self.extra_frame, padx=5, pady=5, bg="white")
        grid_frame.pack(fill="both")
        treeview_frame = tk.Frame(self.extra_frame, padx=5, pady=5, bg="white")
        treeview_frame.pack(fill="both")
        _db = self.controller.controller.current_database

        # treeview
        treeview = ttk.Treeview(treeview_frame)
        treeview.pack(fill="both", expand=True)
        # scrollbars
        yscrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview)
        yscrollbar.pack(side="right", fill="y")
        xscrollbar = ttk.Scrollbar(treeview_frame, orient="horizontal", command=treeview.xview)
        xscrollbar.pack(side="bottom", fill="x")
        treeview.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)
        # columns
        treeview["columns"] = ("one", "two", "three", "four", "five")
        treeview.column("#0", width=0, stretch=False)
        treeview.column("one", anchor="w", width=100)
        treeview.column("two", anchor="w", width=100)
        treeview.column("three", anchor="w", width=100)
        treeview.column("four", anchor="w", width=100)
        treeview.column("five", anchor="e", width=100)
        # headings
        treeview.heading("#0", text="", anchor="w")
        treeview.heading("one", text="Table Name", anchor="w")
        treeview.heading("two", text="Engine", anchor="w")
        treeview.heading("three", text="Charset", anchor="w")
        treeview.heading("four", text="Collation", anchor="w")
        treeview.heading("five", text="Row Count", anchor="w")

        # table names to be used in the next frame
        table_names = []

        if _db is not None:
            _db.connect()
            # get all tables
            td = _db.get_table_metadata()
            row_num = 1
            for k, v in td.items():
                treeview.insert(parent="", index="end", iid=str(row_num), text="",
                                values=(k, v["engine"], v["charset"], v["collation"], v["row_count"]))
                row_num += 1
                table_names.append(k)

        # menu popup
        treeview.bind(
            "<Button-3>",
            lambda e: open_menu_frame(e))
        # bind the treeview to switch to the TablePage
        # when a table name is clicked
        treeview.bind("<Double-1>",
                      lambda e: self.controller.switch_frame(
                          class_name="TablePage",
                          table_name=str(treeview.item(treeview.selection())["values"][0])))

        # function to add the menu frame to the main view
        def open_menu_frame(event):
            """
                The open_menu_frame function is called when the user right-clicks on a treeview item.
                It opens a popup menu that allows the user to delete or edit an item.

                :param event: Identify the event that caused the function to be called
                :return: A menu frame object
            """
            # identify the treeview item that was clicked
            item = treeview.identify_row(event.y)
            # trigger treeview focus
            tr = str(treeview.item(item)["values"][0])
            menu_frame = None

            if item:
                # activate the top level window
                try:
                    menu_frame = MenuFrame(self.controller, table_name=tr)
                    menu_frame.tk_popup(event.x_root, event.y_root)
                    # get focus
                    menu_frame.focus_set()
                finally:
                    menu_frame.grab_release()

        container_frame = tk.Frame(self, height=500, borderwidth=2, relief="groove", padx=5, pady=5, bg="white")
        container_frame.place(y=400, height=450, bordermode="outside", relx=0.5, anchor="n", relwidth=0.98)
        # grid with entries for running SELECT statements

        # and displaying the results
        entry_frame = tk.Frame(container_frame, padx=5, pady=5, bg="white")
        entry_frame.place(x=0, y=0, height=100, bordermode="outside", relx=0.5, rely=0.01, anchor="n", relwidth=0.98)

        # entry for SELECT statement
        select_var = tk.StringVar()
        select_entry_label = tk.Label(entry_frame, text="SELECT", bg="white")
        select_entry_label.pack(side="left", padx=5, pady=5)
        select_entry = tk.Entry(entry_frame, width=100, textvariable=select_var)
        select_entry.pack(side="left", padx=5, pady=5)

        # entry for table name (combobox)
        table_name_var = tk.StringVar()
        table_name_entry_label = tk.Label(entry_frame, text="FROM", bg="white")
        table_name_entry_label.pack(side="left", padx=5, pady=5)
        table_name_entry = ttk.Combobox(entry_frame, width=20, values=table_names, textvariable=table_name_var)
        table_name_entry.pack(side="left", padx=5, pady=5)

        # entry for LIMIT
        limit_var = tk.IntVar()
        limit_entry_label = tk.Label(entry_frame, text="LIMIT", bg="white")
        limit_entry_label.pack(side="left", padx=5, pady=5)
        limit_entry = tk.Entry(entry_frame, width=10, textvariable=limit_var)
        limit_entry.pack(side="left", padx=5, pady=5)

        # button for running SELECT statement
        select_button = tk.Button(entry_frame, text="SELECT")
        # command=lambda: self._select(select_entry.get(), table_name_entry.get(), limit_entry.get())
        select_button.pack(side="left", padx=5, pady=5)
        select_button.bind("<Button-1>", lambda e: build_result(e))

        # result frame label
        result_frame_label = tk.Label(container_frame, text="Results", bg="white")
        result_frame_label.place(x=0, y=70, bordermode="outside", relx=0.5, anchor="n", relwidth=0.98)

        # grid for displaying the results
        result_frame = tk.Frame(container_frame, borderwidth=2, relief="groove", padx=5, pady=5, bg="white")
        result_frame.place(x=0, y=100, height=300, bordermode="outside", relx=0.5, anchor="n", relwidth=0.98)

        # result tree
        result_tree = ttk.Treeview(result_frame)
        result_tree.pack(fill="both", expand=True)
        # scrollbars
        yscrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_tree.yview)
        yscrollbar.pack(side="right", fill="y")
        xscrollbar = ttk.Scrollbar(result_frame, orient="horizontal", command=result_tree.xview)
        xscrollbar.pack(side="bottom", fill="x")
        result_tree.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        # noinspection PyUnusedLocal
        def build_result(e):
            # clear the treeview first
            result_tree.delete(*result_tree.get_children())

            # build a treeview to display data
            # step - 1: get the sql from the variables
            # q = "SELECT"
            select_variables = select_var.get()
            table_variable = table_name_var.get()
            limit_variable = limit_var.get()

            # step - 2: make up q
            q = f"SELECT {select_variables} FROM {table_variable} LIMIT {limit_variable}"

            try:
                result = _db.query(str(q))
                if result:
                    _columns = _db.get_table_columns(str(table_variable))
                    # get only the column names
                    _columns = [col["name"] for col in _columns]

                    # _columns check remove variables not in the table
                    _columns = tuple([col for col in _columns if col in select_variables])

                    # convert to tuple
                    result_tree['columns'] = _columns
                    # format columns
                    result_tree.column("#0", width=0, stretch=False)
                    for col in _columns:
                        result_tree.column(col, anchor="w", width=100)
                        result_tree.heading(col, text=col, anchor="w")

                    for i, row in enumerate(result):
                        # get the value from the row tuple
                        row = list(row)
                        # insert the row
                        result_tree.insert(parent='', index='end', iid=str(i), text="", values=row)
            except Exception as e:
                ErrorHandler(self, str(e))

        # menu popup
        result_tree.bind(
                "<Button-3>",
                lambda e: open_menu_frame_2(e))

        # table_tree.bind("<Button-3>", lambda e: self.controller.controller.open_menu_frame(e, tv=table_tree))
        def open_menu_frame_2(event):
            """
                The open_menu_frame function is called when the user right-clicks on a treeview item.
                It opens a popup menu that allows the user to delete or edit an item.

                :param event: Identify the event that caused the function to be called
                :return: A menu frame object
            """
            # identify the treeview item that was clicked
            item = result_tree.identify_row(event.y)
            print("item: ", item)
            # trigger treeview focus
            tr = str(result_tree.item(item)["values"])
            print("tr: ", tr)
            menu_frame = None

            if item:
                # activate the top level window
                try:
                    menu_frame = MenuFrame(self.controller, row_value=tr)
                    menu_frame.tk_popup(event.x_root, event.y_root)
                    # get focus
                    menu_frame.focus_set()
                finally:
                    menu_frame.grab_release()

