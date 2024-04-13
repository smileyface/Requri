import tkinter as tk
from tkinter import filedialog, messagebox

from UI.autocomplete_entry import AutocompleteEntry
from UI.popups.search_dialog import SearchDialog
from UI.tooltip import Tooltip
from structures.requirement import Requirement, requirements_list
from file_io import import_from_json, export_to_json, import_from_txt, export_to_txt


class RequirementTrackerApp:
    def __init__(self, master):
        self.add_button = tk.Button(self.master, text="Add/Edit Requirement", command=self.add_edit_requirement)
        self.delete_button = tk.Button(self.master, text="Delete Requirement", command=self.delete_requirement)
        self.master = master
        self.master.title("Requirement Tracker")

        self.requirements = []

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):


        # Entry field to add/edit requirement
        self.new_requirement_label = tk.Label(self.master, text="Requirement:")
        self.new_requirement_label.grid(row=2, column=0, padx=5, sticky=tk.E)
        self.new_requirement_entry = tk.Entry(self.master, width=60)
        self.new_requirement_entry.grid(row=2, column=1, columnspan=2, padx=5, sticky=tk.W)

        # Entry field for tags with autocomplete suggestions
        self.tags_label = tk.Label(self.master, text="Tags:")
        self.tags_label.grid(row=3, column=0, padx=5, sticky=tk.E)
        self.autocomplete_tags_entry = AutocompleteEntry(self.master, width=40)
        self.autocomplete_tags_entry.grid(row=3, column=1, columnspan=2, padx=5, sticky=tk.W)
        self.autocomplete_tags_entry.set_autocomplete_list([])  # Populate this list with known tags
        # Adding tooltip for Tags label
        Tooltip(self.tags_label, "Separate tags by '#' symbol")

        # Linking field
        self.link_label = tk.Label(self.master, text="Linked ID:")
        self.link_label.grid(row=4, column=0, padx=5, sticky=tk.E)
        self.link_entry = tk.Entry(self.master, width=20)
        self.link_entry.grid(row=4, column=1, padx=5, sticky=tk.W)

        # Add/Edit Requirement button
        self.add_button.grid(row=5, column=1, padx=5, pady=10)

        # Delete Requirement button
        self.delete_button.grid(row=5, column=2, padx=5, pady=10)

        # Binding double click event to edit requirement
        self.requirement_listbox.bind("<Double-Button-1>", self.edit_requirement)

    def create_menu(self):
        menubar = tk.Menu(self.master)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_requirements)
        file_menu.add_command(label="Open", command=self.open_requirements)
        file_menu.add_separator()

        import_menu = tk.Menu(file_menu, tearoff=0)
        import_menu.add_command(label="From TXT", command=self.import_txt)
        import_menu.add_command(label="From JSON", command=self.import_json)
        file_menu.add_cascade(label="Import", menu=import_menu)

        export_menu = tk.Menu(file_menu, tearoff=0)
        export_menu.add_command(label="To TXT", command=self.export_txt)
        export_menu.add_command(label="To JSON", command=self.export_json)
        file_menu.add_cascade(label="Export", menu=export_menu)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Search", command=self.search_dialog)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.master.config(menu=menubar)

    def delete_requirement(self):
        selected_index = self.requirement_listbox.curselection()
        if selected_index:
            requirement_index = selected_index[0]
            del self.requirements[requirement_index]
            self.requirement_listbox.delete(requirement_index)

    def clear_fields(self):
        self.new_requirement_entry.delete(0, tk.END)
        self.autocomplete_tags_entry.delete(0, tk.END)
        self.link_entry.delete(0, tk.END)

    def save_requirements(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        if filename:
            export_to_json(filename, self.requirements)

    def open_requirements(self):
        filename = filedialog.askopenfilename(filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        if filename:
            self.requirements = import_from_json(filename)
            self.requirement_listbox.delete(0, tk.END)
            for req in self.requirements:
                self.requirement_listbox.insert(tk.END, f"{req.unique_id}: {req.text}")

    def edit_requirement(self, event):
        selected_index = self.requirement_listbox.curselection()
        if selected_index:
            requirement_index = selected_index[0]
            requirement_text = self.requirement_listbox.get(requirement_index)
            self.new_requirement_entry.delete(0, tk.END)
            self.new_requirement_entry.insert(0, requirement_text)

    def add_edit_requirement(self):
        requirement_text = self.new_requirement_entry.get()
        tags = self.autocomplete_tags_entry.update_tags()  # Split tags by '#'
        linked_id = self.link_entry.get()

        requirements_list.append(Requirement("a", "b", "aswdfa", ""))

        selected_index = self.requirement_listbox.curselection()
        if selected_index:
            # Editing existing requirement
            requirement_index = selected_index[0]
            self.requirement_listbox.delete(requirement_index)
            self.requirement_listbox.insert(requirement_index, f"{requirement_text}")
            self.requirements[requirement_index] = Requirement(requirement_text, tags)
        else:
            # Adding new requirement
            if requirement_text:
                new_requirement = Requirement(requirement_text, tags)
                self.requirements.append(new_requirement)
                self.requirement_listbox.insert(tk.END, f"{new_requirement.text}")

        self.clear_fields()

    def import_txt(self):
        filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            self.requirements = import_from_txt(filename)
            self.requirement_listbox.delete(0, tk.END)
            for req in self.requirements:
                self.requirement_listbox.insert(tk.END, f"{req.unique_id}: {req.text}")

    def export_txt(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            data = [f"{req.unique_id}: {req.text}\n" for req in self.requirements]
            export_to_txt(filename, data)

    def import_json(self):
        filename = filedialog.askopenfilename(filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        if filename:
            self.requirements = import_from_json(filename)
            self.requirement_listbox.delete(0, tk.END)
            for req in self.requirements:
                self.requirement_listbox.insert(tk.END, f"{req.unique_id}: {req.text}")

    def export_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        if filename:
            data = [{"unique_id": req.unique_id, "text": req.text, "tags": req.tags} for req in self.requirements]
            export_to_json(filename, data)

    def search_dialog(self):
        dialog = SearchDialog(self.master)
        # You can access the search query result from dialog.result

    def search_requirements(self):
        query = self.search_entry.get().lower()
        if not query:
            messagebox.showinfo("Search", "Please enter a search query.")
            return

        results = []
        for requirement in self.requirements:
            if query in requirement.text.lower() or query in requirement.tags:
                results.append(requirement)

        self.display_search_results(results)

    def display_search_results(self, results):
        self.requirement_listbox.delete(0, tk.END)
        for requirement in results:
            self.requirement_listbox.insert(tk.END, f"{requirement.text}")
