import tkinter as tk

from UI.menubars.main import Callback_Functions, MainMenuBar
from UI.pages.add_requirement import AddRequirementPage
from UI.pages.main import MainPage


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Requirement Tracker")
        self.geometry("600x400")

        self.main_page = MainPage(self)
        self.add_requirement_page = AddRequirementPage(self, self.main_page)

        self.current_page = self.main_page
        self.main_page.pack()

        self.create_menu()

    def create_menu(self):
        menu_bar = MainMenuBar(self)
        menu_bar.register_callback(Callback_Functions.NEW_FILE, self.main_page.update)
        self.config(menu=menu_bar)

    def show_add_requirement(self):
        self.current_page.pack_forget()
        self.add_requirement_page.pack()
        self.current_page = self.add_requirement_page

    def show_main_page(self):
        self.add_requirement_page.pack_forget()
        self.main_page.pack()
        self.current_page = self.main_page