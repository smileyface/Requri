import tkinter as tk
from tkinter import ttk

from UI.menubars.main import MainMenuBar
from UI.pages import requirements, paging_handle
from UI.pages.paging_handle import show_page, create_and_register_frame, PagesEnum


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Requirement Tracker")
        self.geometry("800x600")

        self.full_frame = tk.Frame(self)
        self.page_container = tk.Frame(self.full_frame)
        self.button_box = ttk.Frame(self.full_frame)

        self.page_container.pack(fill=tk.BOTH, expand=True)
        self.create_navigation_bar()

        self.full_frame.pack(fill=tk.BOTH, expand=True)

        create_and_register_frame(self.page_container, PagesEnum.REQUIREMENT_VIEW, requirements.RequirementView)
        create_and_register_frame(self.page_container, PagesEnum.ADD_REQUIREMENT, requirements.AddRequirementPage)
        create_and_register_frame(self.page_container, PagesEnum.EDIT_REQUIREMENT, requirements.EditRequirementPage)
        create_and_register_frame(self.page_container, PagesEnum.MASS_ADD_REQUIREMENT,
                                  requirements.MassAddRequirementPage)
        create_and_register_frame(self.page_container, PagesEnum.REQUIREMENT_EXTENDED,
                                  requirements.RequirementExtendedView)

        show_page(PagesEnum.REQUIREMENT_VIEW)
        self.create_menu(self)

    def create_navigation_bar(self):
        self.page_back_button = tk.Button(self.button_box, text="<", command=paging_handle.page_return)
        self.page_forward_button = tk.Button(self.button_box, text=">")
        self.context_action_box = ttk.Frame(self.button_box)

        # Use grid to arrange buttons and context_action_box
        self.button_box.grid_columnconfigure(0, weight=1)
        self.button_box.grid_columnconfigure(1, weight=1)
        self.button_box.grid_columnconfigure(2, weight=1)

        self.page_back_button.grid(row=0, column=0, sticky="w")
        self.context_action_box.grid(row=0, column=1)
        self.page_forward_button.grid(row=0, column=2, sticky="e")

        self.button_box.pack(fill=tk.X, pady=5)

    def create_menu(self, main_application):
        menu_bar = MainMenuBar(main_application)
        self.config(menu=menu_bar)
