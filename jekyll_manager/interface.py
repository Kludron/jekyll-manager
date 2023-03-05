import sys, os

import tkinter as tk
from tkinter import ttk

from jekyll_manager.manager import Manager

class Interface:
    def __init__(self, root):
        # Create gui root
        self.gui = tk.Tk()
        # Create Manager object
        self.manager = Manager(root)
        # Create custom styles
        self.style = ttk.Style()
        self.style.configure("func.TButton", font=('Menlo', 12))
        self.style.configure("title.TLabel", font=("Arial", 18))
        # Add basic features
        self.gui.title("Jekyll Manager")
        self.label = ttk.Label(
            master=self.gui,
            text="Welcome to Jekyll Manager!",
            style="title.TLabel",
        )
        self.label.pack()
        self.buttons = []

        # Populate buttons
        for function in self.manager.functions:
            button = ttk.Button(
                self.gui, 
                text=function.title(),
                command=self.manager.functions.get(function).get("Function"),
                style="func.TButton"
            )
            self.buttons.append(button)
            button.pack()

        # Add output text box
        self.textout = tk.Text(self.gui)
        self.textout.pack()
        sys.stdout = TextRedirector(self.textout, "stdout")

        # Add input text box
        self.textin = tk.Entry(self.gui)
        self.textin.pack()
        sys.stdin = EntryRedirector(self.textin)

    def run(self):
        self.gui.mainloop()

class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        # write the string to the Text widget with the specified tag
        self.widget.insert(tk.END, str, (self.tag,))

class EntryRedirector:
    def __init__(self, widget):
        self.widget = widget

    def readline(self):
        # wait for the user to enter text in the Entry widget
        while self.widget.get() == "":
            self.widget.update()
        # get the user's text and clear the Entry widget
        text = self.widget.get()
        self.widget.delete(0, tk.END)
        # return the user's text as a string
        return text

if __name__ == "__main__":
    import os
    gui = Interface(os.path.join(os.getenv("HOME"), "lukewarmsecurityinfo.com"))
    gui.run()