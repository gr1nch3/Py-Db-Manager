"""_summary_: sidebar for the database manager program
"""

# Import the necessary modules
import tkinter as tk
from tkinter import ttk


# Import the necessary classes


# turn the sidebar into a treeview
class Sidebar(ttk.Treeview):

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

    def refresh(self):
        """_summary_: refreshes the treeview"""
        # get the selected item
        selected_item = self.selection()[0]
        # delete all children
        self.delete(*self.get_children())
        self._build()
        # expand the parent of the selected item
        if self.parent(selected_item):
            self.item(self.parent(selected_item), open=True)
            # item_2 = self.item(self.parent(selected_item))
            # if self.parent(item_2["text"]):
            #     self.item(self.parent(item_2["text"]), open=True)
        # expand the selected item
        self.item(selected_item, open=True)
        # reselect the selected item
        self.selection_set(selected_item)

    def _build(self):
        """_summary_ : builds the treeview"""
        children = self.controller.get_databases()
        count = 0
        for key, value in children.items():
            #     # parent
            self.insert("", index="end", iid=key, text=key)
            #     # check if parent exists
            if self.exists(key):
                for key2, value2 in value.items():
                    # child
                    # generate unique iid for child item
                    child_iid = f"{key}_{key2}_child_{count}"
                    # self.treeview.bind("<<TreeviewSelect>>", self.dbs_on_select)
                    if self.exists(child_iid):
                        pass
                    else:
                        self.insert(key, index="end", iid=child_iid, text=key2)

                        for item in value2:
                            # child of child
                            # generate unique iid for sub-child item
                            subchild_iid = f"{key}_{key2}_{item}_child_{count}"
                            self.insert(
                                child_iid, index="end", iid=subchild_iid, text=item
                            )
                            # trigger on select event
                            self.bind("<<TreeviewSelect>>", self.on_select)
            else:
                pass

            count += 1

    # on select item in treeview, add details to the central view
    # noinspection PyUnusedLocal
    def on_select(self, event):
        """_summary_: on select item in treeview, add details to the central view"""
        # get the item that was selected
        item = self.selection()[0]
        _cd = self.controller.current_database

        # do nothing if the selection is in the not select list
        not_select_list = ["mysql", "postgresql", "mssql"]
        # get the text of the item that was selected
        if self.item(item, "text").lower() in not_select_list:
            return
        elif self.item(item, "text") == "Databases":
            # get the text of the parent
            item_t = self.item(self.parent(item), "text")

            if _cd is not None:
                # this code is used when switching between mysql, postgresql and mssql
                if item_t.lower() == _cd.db_type:
                    # do nothing for now
                    pass
                else:
                    # set the current database to none
                    self.controller.set_current_database()
            else:
                pass

            # get the children of the item
            children = self.get_children(item)
            # get the text of the children
            children = [self.item(child, "text") for child in children]
            # trigger central view switch frame
            self.controller.central_view.switch_frame(db_list=children)
        else:
            item_text = self.item(item, "text")
            new_item_text = self.controller.process_conn_string(item_text)
            self.controller.set_current_database(new_item_text)
            self.controller.central_view.switch_frame("DetailPage")

    # function to get selected item
    def get_selected_item(self):
        """_summary_: function to get selected item"""
        selected_item = self.selection()[0]
        if self.item(selected_item, "text") == "Databases":
            parent = self.parent(selected_item)
        else:
            parent = None

        return parent

    def change_selected_item(self, item_text):
        """_summary_: function to change selected item"""
        # get the item from the treeview using the item text
        # check for item in children, grand children and great grand children
        item = None
        if item_text is not None:
            for child in self.get_children():
                if self.item(child, "text") == item_text:
                    item = child
                    break
                else:
                    for grand_child in self.get_children(child):
                        if self.item(grand_child, "text") == item_text:
                            item = grand_child
                            break
                        else:
                            for great_grand_child in self.get_children(grand_child):
                                if self.item(great_grand_child, "text") == item_text:
                                    item = great_grand_child
                                    break
                                else:
                                    pass
            # select the item
            if item is not None:
                self.selection_set(item)
                # trigger on select event
                self.event_generate("<<TreeviewSelect>>")
        else:
            pass
