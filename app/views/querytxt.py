""" _summary_ : This file contains the modified version of the text wideget 
                used to write and run the sql queries.
"""

# import necessary modules
import tkinter as tk

class QueryTxt(tk.Text):
    """_summary_

    Args:
        tk (_type_): _description_
    """

    def __init__(self, parent, db_manager, result_controller):
        tk.Text.__init__(self, parent)
        self.db_manager = db_manager
        # controller
        self.controller = parent
        self.result_controller = result_controller
        self.bind("<Button-3>", self.menu_frame)


    def menu_frame(self, event):
        """_summary_ : opens the menu frame
        """
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Run", command=self._run)
        # close menu when clicked outside
        menu.bind("<FocusOut>", lambda event: menu.destroy())
        # get the coordinates of the cursor
        x, y = event.x_root, event.y_root
        # display the menu
        menu.post(x, y)
        menu.focus_set()


    def _run(self):
        """_summary_ : runs the query
        """

        # check if a text is selected
        if self.tag_ranges(tk.SEL):
            # get the selected text
            selected_text = self.get(tk.SEL_FIRST, tk.SEL_LAST)
            print(f"selected q: {selected_text}")
            result = self.db_manager.execute_query(selected_text)
            print(f"result: {result}")
            table_name = self.get_table_name()
            # table_name = table_name[0] if len(table_name) > 0 else ""
            cols = self.db_manager.get_columns(table_name=table_name)

            test_anticipate = self.get_table_name()
            print(f"test_anticipate: {test_anticipate}")

            print(f"cols: {cols}")
            
            if result:
                self.result_controller.add_tab(tab_name=f"{table_name}'s Result", tab_type="result", columns=cols, data=result)

    def get_table_name(self):
        """_summary_ : anticipates the table name
        """
        # get the selected text
        selected_text = self.get(tk.SEL_FIRST, tk.SEL_LAST)
        # list of keywords that usually have the table name
        keywords = ["from", "join", "into", "update", "alter", "table"]
        # check for query that usually have the table name
        if any(x in selected_text.lower() for x in keywords):
            # split the text
            selected_text = selected_text.split()
            # get the index of the keyword
            index = [x for x in range(len(selected_text)) if selected_text[x].lower() in keywords]
            # get the table name which is usually the next word after the keyword and space(s)
            table_name = selected_text[index[0] + 1]
            return table_name.strip().replace(";", "")
        else:
            # might trigger some error
            return ""
