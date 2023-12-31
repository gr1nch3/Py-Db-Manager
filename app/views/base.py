"""_summary_ : Mainview of the program
"""
# Import the necessary modules
import tkinter as tk
from tkinter import ttk

# Import neccessary classes
from .tabview import TabView
from .querytxt import QueryTxt

class MainView(tk.Frame):
    """_summary_

    Args:
        tk (_type_): _description_
    """
    def __init__(self, parent, db_manager):
        tk.Frame.__init__(self, parent, width=500)
        self.controller = parent
        # -------------------------------- main frame -------------------------------- #
        self._frame = tk.Frame(self)
        self._frame.pack(fill="both", expand=True)

        # ----------------------------- temp greet frame ----------------------------- #
        # self._temp_frame = tk.Frame(self._frame, bg="green")
        # self._temp_frame.pack(fill="both", expand=True)
        # # create a label
        # label = tk.Label(self._temp_frame,
        #                  text="Welcome to Py-Db Management System",
        #                  # bg="#ffffff",
        #                  font=("Arial", 30))
        # # pack the label
        # label.pack(pady=100, padx=100)

        # ----------------------------- frames visibility ---------------------------- #
        self.query_frame = None
        self.result_frame = None
        self.query_tab_view = None
        self.result_tab_view = None


        # -------------------------------- temp result frame -------------------------------- #
        self.temp_frame = tk.Frame(self.result_frame, bg="purple")
        self.table_tree = ttk.Treeview(self.temp_frame, columns=())

    def add_tab(self, tab_type: str, tab_name: str = "Query", columns: list=None, data: list=None, tab_frame=None):
        """_summary_

        Args:
            tab_name (str): _description_
            tab_frame (tk.Frame): _description_
        """
        if tab_type == "query":
            if self.query_frame is None:
                self._query_frame()

            if tab_frame is None:
                # check if the tab is in the open_tab list
                if tab_name in [k for k, v in self.query_tab_view.open_tabs.items()]:
                    self.query_tab_view.custom_select(tab_name)
                else:
                    _frame = tk.Frame(self.query_frame)
                    text_area = QueryTxt(parent=_frame, db_manager=self.controller.db_manager, result_controller=self)
                    text_area.pack(fill="both", expand=True)
                    self.query_tab_view.add_tab(tab_name, _frame)
            else:
                _frame = tab_frame
                self.query_tab_view.add_tab(tab_name, _frame)

        elif tab_type == "result":
            if self.result_frame is None:
                if columns is not None and data is not None:
                    self._result_frame()
                # self._result_frame()
            
            if tab_frame is None:
                if columns is not None and data is not None:
                    self._build_tree(columns, data)
                # check if the tab is in the open_tab list
                if tab_name in [k for k, v in self.result_tab_view.open_tabs.items()]:
                    self.result_tab_view.custom_select(tab_name)
                else:
                    self.result_tab_view.add_tab(tab_name, self.temp_frame)
            else:
                _frame = tab_frame
                self.result_tab_view.add_tab(tab_name, _frame)


    def _query_frame(self):
        """_summary_ : frame containing the text box for writing queries
        """
        self.query_frame = tk.Frame(self._frame, bg="red", height=350)
        self.query_frame.pack(fill="both", padx=10, pady=5, expand=True, side="top")
        self.query_tab_view = TabView(self.query_frame)
    
    def _build_tree(self, columns: list, data: list):
        # treeview
        self.table_tree.pack(fill="both", expand=True)

        # add data to the table
        self.table_tree.delete(*self.table_tree.get_children())
        # get the column names and add them to the treeview
        _columns = ([col["name"] for col in columns])
        self.table_tree["columns"] = _columns
        # format the columns
        self.table_tree.column("#0", width=0, stretch=False)
        for col in _columns:
            self.table_tree.column(col, anchor="w", width=100)
            self.table_tree.heading(col, text=col, anchor="w")

        # add the data to the treeview
        for i, row in enumerate(data):
            # get the value from the row tuple
            row = list(row)
            # insert the row
            self.table_tree.insert(parent='', index='end', iid=str(i), text="", values=row)

    def _result_frame(self):
        """_summary_ :
        """
        self.result_frame = tk.Frame(self._frame, bg="white", height=300)
        self.result_frame.pack(fill="both", padx=10, pady=5, expand=True, side="top")

                # scrollbars
        yscrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.table_tree.yview)
        yscrollbar.pack(side="right", fill="y")
        xscrollbar = ttk.Scrollbar(self.result_frame, orient="horizontal", command=self.table_tree.xview)
        xscrollbar.pack(side="bottom", fill="x")
        self.table_tree.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        self.result_tab_view = TabView(self.result_frame)
