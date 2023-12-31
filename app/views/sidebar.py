"""_summary_: sidebar for the database manager program
"""

# Import the necessary modules
import tkinter as tk
from tkinter import ttk


class Sidebar(ttk.Treeview):
    """_summary_

        Args:
            ttk (_type_): _description_
    """
    def __init__(self, parent):
        ttk.Treeview.__init__(self, parent)
        # controller
        self.controller = parent
        self.heading("#0", text="Databases", anchor="w")

        self.plus_button = tk.Button(
            self,
            text="+",
        )
        self.plus_button.place(relx=0.95, rely=0.01, anchor="center")
        # shrink button height
        self.plus_button.config(height=1, width=1)
        # trigger on click event to controller open database frame
        self.plus_button.bind("<Button-1>", self.controller.open_database_frame)
    
        self._build()
        self.bind("<Button-3>", self.menu_frame)
        self.bind("<<TreeviewSelect>>", self.on_select)

    def refresh(self):
        """_summary_: refreshes the treeview"""
        # get the selected item
        # selected_item = self.selection()[0]
        # delete all children
        self.delete(*self.get_children())
        self._build()
        # expand the parent of the selected item
        # if self.parent(selected_item):
        #     self.item(self.parent(selected_item), open=True)
        #     # item_2 = self.item(self.parent(selected_item))
        #     # if self.parent(item_2["text"]):
        #     #     self.item(self.parent(item_2["text"]), open=True)
        # # expand the selected item
        # self.item(selected_item, open=True)
        # # reselect the selected item
        # self.selection_set(selected_item)

    def open_result(self, event):
        """_summary_ : opens the result tab
        """
        item = self.identify_row(event.y)
        tr = str(self.item(item, "text"))
        self.controller.main_view.add_tab(tab_name=f"{tr} Result", tab_type="result")


    def menu_frame(self, event):
        """_summary_ : opens the menu frame
        """

        item = self.identify_row(event.y)

        if self.parent(item):
            pass
        else:
            if item:
                menu = tk.Menu(self, tearoff=0)
                menu.add_command(label="View details", command=self._run)
                menu.add_command(label="Refresh", command=self.refresh)
                # close menu when clicked outside
                menu.bind("<FocusOut>", lambda event: menu.destroy())
                # get the coordinates of the cursor
                x, y = event.x_root, event.y_root
                # display the menu
                menu.post(x, y)
                menu.focus_set()
                # menu.grab_release()

    def _run(self):
        """_summary_ : runs the query
        """
        pass

    def _build(self):
        """_summary_ : builds the treeview
        """
        print("build called")
        # children = ["Database 1", "Database 2", "Database 3", "Database 4", "Database 5"]
        db = self.controller.db_manager
        if db.session is not None:
            children = db.get_db_and_table_names()
        else:
            children = {}

        count = 0
        for key, value in children.items():
            # db name or parent
            self.insert("", index="end", iid=key, text=key)
            # check if parent exists
            if self.exists(key):
                for child in value:
                    # table name or child
                    # generate unique iid for child item
                    child_iid = f"{key}_{child}_child_{count}"
                    if self.exists(child_iid):
                        pass
                    else:
                        self.insert(key, index="end", iid=child_iid, text=child)
                        # trigger on select event
            else:
                pass
            count += 1


    def on_select(self, event):
        """_summary_ : triggers when an item is selected
        """
        # get the selected item
        selected_item = self.selection()[0]
        # check if the selected item is valid
        if self.item(selected_item):
            # check if the item is a child
            if self.parent(selected_item):
                pass
            else:
                self.controller.main_view.add_tab(tab_name=self.item(selected_item)["text"], tab_type="query")
