import tkinter as tk
from tkinter import ttk

from UI.pages import paging_handle
from UI.pages.viewpage import ViewPage


class RequirementExtendedView(ViewPage):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.requirement = None

    def create_body(self):
        # Create a Notebook widget (tabbed frame)
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        requirement_tab = self.make_requirement_tab(notebook)
        trace_tab = self.make_trace_tab(notebook)

        notebook.add(requirement_tab, text='Requirement')
        notebook.add(trace_tab, text='Traceability')

    def make_requirement_tab(self, master):
        tab = ttk.Frame(master)

        title_frame = ttk.Frame(tab)
        text_frame = ttk.Frame(tab)
        # Create labels
        self.unique_id = tk.Label(title_frame, text="UNIQUE ID", font=("Helvetica", 8))
        self.title_label = tk.Label(title_frame, text="LABEL", font=("Helvetica", 12, "bold"))
        self.text_label = tk.Label(text_frame, justify="left", text="Lorem ipsum dolor sit amet, consectetur "
                                                                    "adipiscing elit, sed doeiusmod tempor incididunt "
                                                                    "ut labore et dolore magna aliqua. Ut enim ad "
                                                                    "minim veniam, quis nostrud exercitation ullamco "
                                                                    "laboris nisi ut aliquip ex ea commodo consequat. "
                                                                    "Duis aute irure dolor in reprehenderit in "
                                                                    "voluptate velit esse cillum dolore eu fugiat "
                                                                    "nulla pariatur. Excepteur sint occaecat "
                                                                    "cupidatat non proident, sunt in culpa qui "
                                                                    "officia deserunt mollit anim id est laborum.")

        # Pack labels inside the label frame
        self.unique_id.pack(side="left", pady=10)
        self.title_label.pack(side="top", padx=10, pady=10)
        self.text_label.pack(side="left")

        # Pack the label frame to the top of the main frame
        title_frame.pack(anchor="n", fill="x", padx=10, pady=10)
        text_frame.pack(anchor="w", fill="x")

        def update_wraplength(event):
            tab_width = event.width
            self.text_label.config(wraplength=tab_width - 20)  # Adjust the padding as needed

        tab.bind("<Configure>", update_wraplength)

        return tab

    def make_trace_tab(self, master):
        tab = ttk.Frame(master)
        label2 = tk.Label(tab, text='This is Tab 2')
        label2.pack(padx=10, pady=10)
        return tab

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
        else:
            raise ValueError("Data not passed")
