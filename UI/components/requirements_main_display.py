import tkinter as tk
from tkinter import ttk

from structures.requirement import RequirementList


class RequirementsDisplayMain(ttk.Treeview):

    def __init__(self, master, **kwargs):
        super().__init__(master, columns=("ID", "Text"), **kwargs)

        self.heading("#0", text="ID")
        self.heading("#1", text="Text")

        self.entries = {}
        self.update()

    def add(self, requirement):
        requirement_str = requirement.unique_id.to_string()
        self.insert("", tk.END, text=requirement_str, values=(requirement.text,))
        self.entries[requirement_str] = requirement

    def remove(self, index):
        requirement_str = requirement.unique_id.to_string()
        if requirement_str in self.entries:
            removed_requirement = self.entries.pop(requirement_str)
            self.delete(requirement_str)

    def update(self):
        # Clear the Treeview
        for item in self.get_children():
            self.delete(item)

        self.entries.clear()

        requirement_map = RequirementList.get_requirement_map()
        sorted_keys = sorted(requirement_map.keys(), key=lambda x: (x[0], x[1]))
        # Iterate over the sorted keys and access the corresponding requirement maps
        for requirement_section in sorted_keys:
            for requirement in requirement_map[requirement_section].values():
                self.add(requirement)