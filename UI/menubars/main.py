import json
import os.path
import tkinter as tk
from enum import Enum
from tkinter import filedialog

import parsers.source_cpp
from UI.dialog.new_project import NewProjectDialog
from UI.pages.paging_handle import show_page, PagesEnum, get_page, get_current_page
from structures import requirement_list, project
from structures import code


class Callback_Functions(Enum):
    NEW_FILE = "New File"


class MainMenuBar(tk.Menu):
    parser = parsers.source_cpp.cpp_parser()
    def __init__(self, master):
        super().__init__(master)

        # Create File menu
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
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
        add_project_menu.add_command(label="Requirement (Mass)", command=self.mass_add_requirement)
        project_menu.add_cascade(label="Add", menu=add_project_menu)
        self.add_cascade(label="Project", menu=project_menu)

        # callbacks
        self.new_file_callback = lambda: {}

    def register_callback(self, callback, func):
        if callback is Callback_Functions.NEW_FILE:
            self.new_file_callback = func

    def new_file(self):
        print("New file")
        requirement_list.clear_list()
        self.new_file_callback()
        dialog = NewProjectDialog(self.master, title="New Project")
        project.set_name(dialog)
        get_page(get_current_page()).update()



    def save_file(self):
        if project.get_save_file():
            with open(project.get_save_file(), "w") as file:
                json.dump(project.generate_save_file(), file, indent=4)
        else:
            self.save_as_file()

    def save_as_file(self):
        project.set_save_file(filedialog.asksaveasfilename(initialdir="/", title="Select Save File",
                                                           filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
                                                           defaultextension=".json"))
        self.save_file()

    def open_file(self):
        requirement_list.clear_list()
        project.set_save_file(filedialog.askopenfilename(initialdir="/", title="Select Open File",
                                                         filetypes=(("JSON files", "*.json"), ("All files", "*.*"))))
        if project.get_save_file():
            with open(project.get_save_file(), "r") as file:
                project.expand_save_file(json.load(file))
        get_page(PagesEnum.REQUIREMENT_VIEW).on_show()

    def import_code(self):
        project.set_code_location(filedialog.askdirectory(initialdir="/", title="Select Code Directory"))
        cpp_code_files = self.parser.scan_cpp_files(project.get_code_location())
        functions = []
        for file_path in cpp_code_files:
            functions.extend(self.parser.find_functions(file_path))
        for x in functions:
            code.append(code.Code(os.path.relpath(x[0], project.get_code_location()), x[1]))
        get_page(get_current_page()).update()

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
        show_page(PagesEnum.ADD_REQUIREMENT)

    def mass_add_requirement(self):
        show_page(PagesEnum.MASS_ADD_REQUIREMENT)