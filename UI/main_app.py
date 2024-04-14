import tkinter as tk

from UI.menubars.main import Callback_Functions, MainMenuBar
from UI.pages.add_requirement import AddRequirementPage
from UI.pages.main import MainPage
from UI.pages.paging_handle import show_page, create_and_register_frame, PagesEnum, get_page


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Requirement Tracker")
        self.geometry("800x600")

        self.page_container = tk.Frame(self)
        self.page_container.pack(fill=tk.BOTH, expand=True)

        create_and_register_frame(self.page_container, PagesEnum.MAIN, MainPage)
        create_and_register_frame(self.page_container, PagesEnum.ADD_REQUIREMENTS, AddRequirementPage)

        show_page(PagesEnum.MAIN)
        self.create_menu(self)

    def create_menu(self, main_application):
        menu_bar = MainMenuBar(main_application)
        menu_bar.register_callback(Callback_Functions.NEW_FILE, get_page(PagesEnum.MAIN).update)
        self.config(menu=menu_bar)
