import tkinter as tk

from UI.menubars.main import Callback_Functions, MainMenuBar
from UI.pages.add_requirement import AddRequirementPage
from UI.pages.main import MainPage
from UI.pages.paging_handle import show_page, create_and_register_frame, PagesEnum


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Requirement Tracker")
        self.geometry("800x600")

        self.page_container = tk.Frame(self)
        self.page_container.pack(fill=tk.BOTH, expand=True)

        self.main_page = create_and_register_frame(self.page_container, PagesEnum.MAIN, MainPage)
        self.add_requirement_page = create_and_register_frame(self.page_container, PagesEnum.ADD_REQUIREMENTS,
                                                              AddRequirementPage)
        print("Main page:", self.main_page)  # Add this line to check the main page frame
        print("Add requirement page:", self.add_requirement_page)  # Add this line to check the add requirement page frame

        show_page(PagesEnum.MAIN)
        self.create_menu(self)

    def create_menu(self, main_application):
        menu_bar = MainMenuBar(main_application)
        menu_bar.register_callback(Callback_Functions.NEW_FILE, main_application.main_page.update)
        self.config(menu=menu_bar)