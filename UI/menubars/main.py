import tkinter as tk
from enum import Enum

from UI.pages.paging_handle import show_page, PagesEnum
from structures.requirement import RequirementList


class Callback_Functions(Enum):
    NEW_FILE = "New File"


class MainMenuBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        # Create File menu
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Open", command=self.open_file)

        file_menu.add_separator()

        import_menu = tk.Menu(file_menu, tearoff=0)
        import_menu.add_command(label="Code", command=self.import_code)
        import_menu.add_command(label="Test", command=self.import_test)
        file_menu.add_cascade(label="Import", menu=import_menu)

        export_menu = tk.Menu(file_menu, tearoff=0)
        export_menu.add_command(label="Text", command=self.export_txt)
        export_menu.add_command(label="JSON", command=self.export_json)
        file_menu.add_cascade(label="Export", menu=export_menu)

        file_menu.add_separator()

        file_menu.add_command(label="Exit", command=self.quit)
        self.add_cascade(label="File", menu=file_menu)
        # Create Edit menu
        edit_menu = tk.Menu(self, tearoff=False)
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        self.add_cascade(label="Edit", menu=edit_menu)

        project_menu = tk.Menu(self, tearoff=False)
        add_project_menu = tk.Menu(project_menu, tearoff=0)
        add_project_menu.add_command(label="Requirement", command=self.add_requirement)
        project_menu.add_cascade(label="Add", menu=add_project_menu)
        self.add_cascade(label="Project", menu=project_menu)


        # callbacks
        self.new_file_callback = lambda: {}

    def register_callback(self, callback, func):
        if callback is Callback_Functions.NEW_FILE:
            self.new_file_callback = func

    def new_file(self):
        print("New file")
        RequirementList.clear_list()
        self.new_file_callback()

    def save_file(self):
        print("Save File")

    def open_file(self):
        print("Open file")

    def import_code(self):
        print("Importing Code")

    def import_test(self):
        print("Importing Test")

    def export_txt(self):
        print("Export Text")

    def export_json(self):
        print("Export JSON")

    def quit(self):
        print("Quit")

    def cut(self):
        print("Cut")

    def copy(self):
        print("Copy")

    def paste(self):
        print("Paste")

    def add_requirement(self):
        print("Main Menu - Add Requirement")
        show_page(PagesEnum.ADD_REQUIREMENTS)
