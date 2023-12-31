"""_summary_ : A view to hanlde the tabs of the text and result views
"""

# import the necessary modules
import tkinter as tk
from tkinter import ttk


class TabView(ttk.Notebook):
    """_summary_

    Args:
        ttk (_type_): _description_
    """

    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent)
        self.controller = parent
        self.open_tabs = {}

        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=[15, 5])
        style.map(
            "TNotebook.Tab",
            foreground=[("selected", "black")],
            background=[("selected", "#ffffff")],
        )

    def custom_select(self, tab_name: str):
        """_summary_

        Args:
            tab_name (str): _description_
        """
        # search open tabs for the tabid
        self.select(self.open_tabs[tab_name])

    def add_tab(self, tab_name: str, tab_frame):
        """_summary_

            Args:
                tab_name (str): _description_
                tab_frame (tk.Frame): _description_
        """
        self.add(tab_frame, text=tab_name)
        # get the tabid
        tab_id = self.tabs()[-1]
        self.open_tabs[tab_name] = tab_id
        self.pack(fill="both", expand=True, side="top")
        self.select(tab_frame)

    def remove_tab(self, tab_frame):
        """_summary_

            Args:
                tab_frame (tk.Frame): _description_
        """
        self.forget(tab_frame)
        self.open_tabs.pop(tab_frame)
        if len(self.open_tabs) == 0:
            self.controller.remove_tab()
