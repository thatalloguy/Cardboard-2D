import logging
from tkinter import messagebox

class Logger:
    def __init__(self):
        self.filename = "logs/__log__.log"


    def send_info(self, message=""):
        print("INFO: " + message)

    def send_error(self, message="", poppup=True):
        self.poppup = poppup
        print("ERROR: " + message)
        if self.poppup == True:
            messagebox.showerror(message, 'ERROR')

    def send_warning(self, message, poppup=True,type=None):
        self.type = type
        if self.type == None:
            self.type = "MEDIUM"
        self.poppup = poppup
        print("WARNING(" + self.type + "): " + message)
        if self.poppup == True:
            messagebox.showwarning(message, 'Warning' + " ||" + self.type + "||")

