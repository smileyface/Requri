import tkinter as tk
from UI.pages.viewpage import ViewPage
from UI.components.dropdown_with_add import ComboboxWithAdd
from structures.requirement import RequirementList


def get_variable(var):
    return var.variable.get().replace('\'', '')


class AddRequirementPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Create main frame for the page
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create left panel for inputs
        self.left_panel = tk.Frame(self.main_frame)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)

        # Create right panel for text block
        self.right_panel = tk.Frame(self.main_frame)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Title
        self.title_label = tk.Label(self.left_panel, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.left_panel)
        self.title_entry.pack()

        # Section
        self.section_label = tk.Label(self.left_panel, text="Section:")
        self.section_label.pack()
        self.section = ComboboxWithAdd(self.left_panel, RequirementList.get_section_lists(),
                                       selected_callback=self.update_combobox_b)
        self.section.pack()

        # Subsection
        self.subsection_label = tk.Label(self.left_panel, text="Subsection:")
        self.subsection_label.pack()
        self.subsection = ComboboxWithAdd(self.left_panel, RequirementList.get_subsection_lists(self.section))
        self.subsection.pack()

        # Requirement
        self.requirement_label = tk.Label(self.right_panel, text="Requirement:")
        self.requirement_label.pack()
        self.requirement_text = tk.Text(self.right_panel)
        self.requirement_text.pack(fill=tk.BOTH, expand=True)

        # Buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.add_button = tk.Button(self.button_frame, text="Add", command=self.add)
        self.add_button.pack(side=tk.LEFT)
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel)
        self.cancel_button.pack(side=tk.LEFT)

    def update_combobox_b(self, event=None):
        section = get_variable(self.section)
        if section in RequirementList.get_section_lists():
            b_values = RequirementList.get_subsection_lists(section)
            self.subsection.set_values(b_values)
            if b_values:
                self.subsection.variable.set(b_values[0])

    def add(self):
        self.master.show_main_page()

    def cancel(self):
        self.master.show_main_page()
