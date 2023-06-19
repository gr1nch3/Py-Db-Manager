""" _Summary_ : This file contains the class ErrorHandler, which is a class that
                handles all errors that occur in the program. It contains the
                following functions:
                    - display_error
                    - display_warning
                    - display_info
                    - display_success
"""

# import necessary modules
import tkinter as tk
import pathlib

# import necessary classes
# from .base import BaseView


class ErrorHandler(tk.Toplevel):
    """ _summary_: frame for the error handler
    """

    def __init__(self, parent, error_message: str):
        """
            The __init__ function is called when the class is being initiated.

            :param self: Represent the instance of the class
            :param parent: Pass the controller to the error handler
            :param error_message: Pass the error message to the error handler
            :return: Nothing
        """
        tk.Toplevel.__init__(self, parent)
        # controller
        self.controller = parent
        self.resizable(False, False)
        # self.overrideredirect(True)
        self.transient(parent)
        # close menu when clicked outside
        # self.bind("<FocusOut>", lambda event: self.dispose())
        # change close button function
        self.protocol("WM_DELETE_WINDOW", self.dispose)
        # error message
        self.error_message = error_message
        # title
        self.title("Error")
        # set a maximum size for the window
        self.maxsize(500, 400)
        # view
        self._view()

    def _view(self):
        """
            The _view function is called when the class is being initiated.

            :param self: Represent the instance of the class
            :return: Nothing
        """
        # frame
        frame = tk.Frame(self)
        frame.pack(pady=10, padx=10)
        # error icon
        error_icon = tk.PhotoImage(file="program/images/error.png")
        error_icon = error_icon.subsample(10, 10)
        error_icon_label = tk.Label(frame, image=error_icon, width=100, height=100)
        error_icon_label.image = error_icon
        error_icon_label.pack(side="left")
        # error message
        error_message = tk.Text(frame, width=30, height=10, font=("Arial", 12), fg="red", wrap="word")
        error_message.insert("1.0", self.error_message)
        error_message.pack(pady=5, padx=5)
        # point to the log file for more information
        log_file = tk.Label(frame, text="See log file for more information", font=("Arial", 12), fg="blue")
        log_file.pack(pady=5, padx=10)
        # log file location
        # current_directory = pathlib.Path(__file__).resolve().parent
        log_file_location = pathlib.Path("logs/database_manager.log")
        log_file_location = log_file_location.resolve()
        log_file_location = str(log_file_location)
        log_file_location = tk.Label(frame, text=log_file_location, font=("Arial", 10), fg="red")
        log_file_location.pack(pady=2, padx=10)

    def dispose(self):
        """
            The dispose function is called when the user closes the window.
            It removes all references to this object, so that it can be garbage collected.

            :param self: Represent the instance of the class
            :return: The toplevel
        """
        # dispose of the toplevel
        self.destroy()
