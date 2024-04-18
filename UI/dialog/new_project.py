import tkinter as tk
from tkinter import simpledialog


class NewProjectDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Enter project name:").grid(row=0, column=0)
        self.project_name_entry = tk.Entry(master)
        self.project_name_entry.grid(row=0, column=1)
        return self.project_name_entry  # Return the widget to set initial focus

    def apply(self):
        project_name = self.project_name_entry.get()
        # Do something with the project name, like creating a new project
        print("Creating new project:", project_name)
