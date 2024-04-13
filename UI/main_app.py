import tkinter as tk

from UI.menubars.main import Callback_Functions, MainMenuBar
from UI.pages.add_requirement import AddRequirementPage
from UI.pages.main import MainPage


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Requirement Tracker")
        self.geometry("800x600")

        self.page_container = tk.Frame(self)
        self.page_container.pack(fill=tk.BOTH, expand=True)

        self.main_page_frame = tk.Frame(self.page_container)
        self.main_page = MainPage(self.main_page_frame)
        self.main_page.pack(fill=tk.BOTH, expand=True)

        self.add_requirement_page_frame = tk.Frame(self.page_container)
        self.add_requirement_page = AddRequirementPage(self.add_requirement_page_frame)
        self.add_requirement_page.pack(fill=tk.BOTH, expand=True)

        self.current_page = None
        self.show_main_page()

        self.create_menu(self)

    def create_menu(self, main_application):
        menu_bar = MainMenuBar(main_application)
        menu_bar.register_callback(Callback_Functions.NEW_FILE, main_application.main_page.update)
        self.config(menu=menu_bar)

    def show_add_requirement(self):
        print("Showing add requirement page")
        if self.current_page:
            self.current_page.grid_forget()
        self.add_requirement_page_frame.grid(row=0, column=0, sticky="nsew")
        self.current_page = self.add_requirement_page_frame

    def show_main_page(self):
        print("Showing main page")
        if self.current_page:
            self.current_page.grid_forget()
        self.main_page_frame.grid(row=0, column=0, sticky="nsew")
        self.current_page = self.main_page_frame
