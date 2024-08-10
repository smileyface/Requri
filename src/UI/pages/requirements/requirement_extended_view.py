import logging
import tkinter as tk
from tkinter import ttk

from src.UI.pages import paging_handle
from src.UI.pages.viewpage import ViewPage
from src.structures.records import *


class RequirementExtendedView(ViewPage):
    def __init__(self, master):
        super().__init__(master)
        self.trace_tab = None
        self.text_label = None
        self.title_label = None
        self.unique_id = None
        self.connected_listbox = None
        self.master = master
        self.requirement = None
        self.notebook = None
        self.requirement_tab = None
        self.title_frame = None
        self.text_frame = None

    def create_body(self):
        logging.info(f"{type(self).__name__} body created")
        # Create a Notebook widget (tabbed frame)
        self.notebook = ttk.Notebook(self)

        self.requirement_tab = self.make_requirement_tab(self.notebook)
        self.trace_tab = self.make_trace_tab(self.notebook)

        self.notebook.add(self.requirement_tab, text='Requirement')
        self.notebook.add(self.trace_tab, text='Traceability')

    def display_body(self):
        #Display main notebook
        self.notebook.pack(fill='both', expand=True)
        #Display Trace Tab
        self.connected_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #Display Requirements Tab

        # Pack labels inside the label frame
        self.unique_id.pack(side="left", pady=10)
        self.title_label.pack(side="top", padx=10, pady=10)
        self.text_label.pack(side="left")

        # Pack the label frame to the top of the main frame
        self.title_frame.pack(anchor="n", fill="x", padx=10, pady=10)
        self.text_frame.pack(anchor="w", fill="x")

    def make_requirement_tab(self, master):
        tab = ttk.Frame(master)

        self.title_frame = ttk.Frame(tab)
        self.text_frame = ttk.Frame(tab)

        # Create labels
        self.unique_id = tk.Label(self.title_frame, text="UNIQUE ID", font=("Helvetica", 8))
        self.title_label = tk.Label(self.title_frame, text="LABEL", font=("Helvetica", 12, "bold"))
        # noinspection SpellCheckingInspection
        self.text_label = tk.Label(self.text_frame, justify="left", text="Lorem ipsum dolor sit amet, consectetur "
                                                                         "adipiscing elit, sed doeiusmod tempor incididunt "
                                                                         "ut labore et dolore magna aliqua. Ut enim ad "
                                                                         "minim veniam, quis nostrud exercitation ullamco "
                                                                         "laboris nisi ut aliquip ex ea commodo consequat. "
                                                                         "Duis aute irure dolor in reprehenderit in "
                                                                         "voluptate velit esse cillum dolore eu fugiat "
                                                                         "nulla pariatur. Excepteur sint occaecat "
                                                                         "cupidatat non proident, sunt in culpa qui "
                                                                         "officia deserunt mollit anim id est laborum.")

        def update_wraplength(event):
            tab_width = event.width
            self.text_label.config(wraplength=tab_width - 20)  # Adjust the padding as needed

        tab.bind("<Configure>", update_wraplength)

        return tab

    def make_trace_tab(self, master):
        tab = ttk.Frame(master)
        self.connected_listbox = ttk.Treeview(tab)
        return tab

    def get_list_of_type(self, list, type):
        list_of_type = []
        for x in list:
            if type(x) is type(type):
                list_of_type.append(x)
        return list_of_type

    def populate_listbox(self):
        connected = []
        for key, values in self.requirement.connections.items():
            connected.extend(values)
        code_list = self.get_list_of_type(connected, Code)
        requirements_list = self.get_list_of_type(connected, Requirement)
        if len(code_list) > 0:
            code_id = self.connected_listbox.insert("", "end", text="Implementations")
            for x in code_list:
                self.connected_listbox.insert(code_id, "end", text=str(x))
        if len(requirements_list) > 0:
            requirement_id = self.connected_listbox.insert("", "end", text="Related Requirements")
            for x in requirements_list:
                self.connected_listbox.insert(requirement_id, "end", text=x, iid=f"Req-{x.unique_id.to_string()}")

    def create_context_nav(self):
        edit_button = tk.Button(self.context_action_box, text="Edit", command=self.go_to_edit)
        edit_button.pack()

    def go_to_edit(self):
        paging_handle.get_page(paging_handle.PagesEnum.EDIT_REQUIREMENT).requirement = self.requirement
        paging_handle.show_page(paging_handle.PagesEnum.EDIT_REQUIREMENT)

    def on_show(self):
        super().on_show()
        if self.requirement:
            self.unique_id.config(text=self.requirement.unique_id.to_string())
            self.title_label.config(text=self.requirement.title)
            self.text_label.config(text=self.requirement.text)
            self.populate_listbox()

        else:
            raise ValueError("Data not passed")
