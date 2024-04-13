import tkinter as tk

from UI.components.dropdown_with_add import ComboboxWithAdd
from structures.requirement import RequirementList


def get_variable(var):
    return var.variable.get().replace('\'', '')


class AddRequirementPage(tk.Frame):
    def __init__(self, master, main_page):
        super().__init__(master)
        self.requirement = tk.Entry(self.master)
        self.section = ComboboxWithAdd(self.master, RequirementList.get_section_lists(),
                                       selected_callback=self.update_combobox_b)
        self.subsection = ComboboxWithAdd(self.master, RequirementList.get_subsection_lists(self.section))
        self.requirement_title = tk.Entry(self.master)
        self.master = master
        self.main_page = main_page

        self.label = tk.Label(self, text="Add Requirement Page")
        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel)

        self.label.pack()
        self.cancel_button.pack()

    def update_combobox_b(self, event=None):
        section = get_variable(self.section)
        if section in RequirementList.get_section_lists():
            b_values = RequirementList.get_subsection_lists(section)
            self.subsection.set_values(b_values)
            if b_values:
                self.subsection.variable.set(b_values[0])

    def create_widgets(self):
        tk.Label(self.master, text="Title:").grid(row=0, column=0, columnspan=3, sticky="w")
        self.requirement_title.grid(row=0, column=1, sticky="w")

        tk.Label(self.master, text="Section:").grid(row=1, column=0, sticky="w")
        self.section.grid(row=1, column=1, sticky="w")

        tk.Label(self.master, text="Subsection:").grid(row=2, column=0, sticky="w")
        self.subsection.grid(row=2, column=1)

        tk.Label(self.master, text="Requirement").grid(row=0, column=2, columnspan=3, sticky="ew")
        self.requirement.grid(row=1, column=2, columnspan=3, rowspan=3, sticky="nsew")

    def add(self):
        self.main_page.show()

    def cancel(self):
        self.main_page.show()
