import tkinter as tk
from UI.components.requirements_main_display import RequirementsDisplayMain
from UI.menubars.main import MainMenuBar, Callback_Functions
from UI.popups.add_requirement import AddRequirementDialog
from structures.requirement import RequirementList


class MainPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.label = tk.Label(self, text="Main Page")

        self.label.pack()

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Label
        self.label.grid(row=0, column=0, columnspan=3, pady=10)
        self.requirement_listbox.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.add_button.grid(row=5, column=1, padx=5, pady=10)

    def create_menu(self):
        menu_bar = MainMenuBar(self.master)
        menu_bar.register_callback(Callback_Functions.NEW_FILE, self.requirement_listbox.update)

        self.master.config(menu=menu_bar)

    def show_add_requirement(self):
        self.master.show_add_requirement()
