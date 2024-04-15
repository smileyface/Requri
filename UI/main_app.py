import tkinter as tk

from UI.menubars.main import Callback_Functions, MainMenuBar
from UI.pages.requirements.add_requirement import AddRequirementPage
from UI.pages.requirements.requirement_view import RequirementView
from UI.pages.paging_handle import show_page, create_and_register_frame, PagesEnum, get_page


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Requirement Tracker")
        self.geometry("800x600")

        self.page_container = tk.Frame(self)
        self.page_container.pack(fill=tk.BOTH, expand=True)

        create_and_register_frame(self.page_container, PagesEnum.REQUIREMENT_VIEW, RequirementView)
        create_and_register_frame(self.page_container, PagesEnum.ADD_REQUIREMENTS, AddRequirementPage)

        show_page(PagesEnum.REQUIREMENT_VIEW)
        self.create_menu(self)

    def create_menu(self, main_application):
        menu_bar = MainMenuBar(main_application)
        menu_bar.register_callback(Callback_Functions.NEW_FILE, get_page(PagesEnum.REQUIREMENT_VIEW).update)
        self.config(menu=menu_bar)
