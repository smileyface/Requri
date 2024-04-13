import tkinter as tk
from tkinter import simpledialog

from UI.components.dropdown_with_add import ComboboxWithAdd
from structures.requirement import Requirement
from structures import requirement_list


def get_variable(var):
    return var.variable.get().replace('\'', '')


class AddRequirementDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Title:").grid(row=0, column=0, columnspan=3, sticky="w")
        self.requirement_title = tk.Entry(master)
        self.requirement_title.grid(row=0, column=1, sticky="w")

        tk.Label(master, text="Section:").grid(row=1, column=0, sticky="w")
        self.section = ComboboxWithAdd(master, requirement_list.get_section_lists(), selected_callback=self.update_combobox_b)
        self.section.grid(row=1, column=1, sticky="w")

        tk.Label(master, text="Subsection:").grid(row=2, column=0, sticky="w")
        self.subsection = ComboboxWithAdd(master, requirement_list.get_subsection_lists(self.section))
        self.subsection.grid(row=2, column=1)

        tk.Label(master, text="Requirement").grid(row=0, column=2, columnspan=3, sticky="ew")
        self.requirement = tk.Entry(master)
        self.requirement.grid(row=1, column=2, columnspan=3, rowspan=3, sticky="nsew")

        return self.requirement_title

    def apply(self):
        req = Requirement(get_variable(self.section), get_variable(self.subsection), self.title.get(), self.requirement.get(), [])
        self.result = req  # You can do something with the search query and option here

    def update_combobox_b(self, event=None):
        section = get_variable(self.section)
        if section in requirement_list.get_section_lists():
            b_values = requirement_list.get_subsection_lists(section)
            self.subsection.set_values(b_values)
            if b_values:
                self.subsection.variable.set(b_values[0])

    @staticmethod
    def show_dialog(root):
        dialog = AddRequirementDialog(root, title="Add Requirement")
        return dialog.result
