import tkinter as tk
from tkinter import ttk, messagebox

import structures
from UI.pages.viewpage import ViewPage
from UI.components.dropdown_with_add import ComboboxWithAdd
from UI.components.autocomplete_entry import AutoCompleteEntry
from structures.records.record import Record
from structures.records.requirement import Requirement
from structures.lists import requirement_list
from UI.pages.paging_handle import page_return
from structures.records import *


def get_variable(var):
    return var.variable.get().replace('\'', '')


class AddRequirementPage(ViewPage):
    def __init__(self, master):
        super().__init__(master)
        self.connected_listbox = None
        self.requirement_text = None
        self.requirement_label = None
        self.tagging_text = None
        self.tagging_label = None
        self.subsection = None
        self.subsection_label = None
        self.section = None
        self.section_label = None
        self.title_entry = None
        self.title_label = None
        self.right_panel = None
        self.left_panel = None
        self.main_frame = None
        self.connectable_listbox = None
        self.master = master
        self._drag_data = None
        self.connections = []

    def create_body(self):
        print("RequrementExtendedView body created")
        # Create a Notebook widget (tabbed frame)
        notebook = ttk.Notebook(self.master)
        notebook.pack(fill='both', expand=True)

        requirement_tab = self.make_requirement_tab(notebook)
        trace_tab = self.make_trace_tab(notebook)

        notebook.add(requirement_tab, text='Requirement')
        notebook.add(trace_tab, text='Traceability')

    def make_requirement_tab(self, master):
        tab = ttk.Frame(master)
        # Create main frame for the page
        self.main_frame = tk.Frame(tab)
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
        self.section = ComboboxWithAdd(self.left_panel, requirement_list.get_section_lists(),
                                       selected_callback=self.update_combobox_b)
        self.section.pack()

        # Subsection
        self.subsection_label = tk.Label(self.left_panel, text="Subsection:")
        self.subsection_label.pack()
        self.subsection = ComboboxWithAdd(self.left_panel, requirement_list.get_subsection_lists(self.section))
        self.subsection.pack()

        # Tags
        self.tagging_label = tk.Label(self.left_panel, text="Tags:")
        self.tagging_text = AutoCompleteEntry(self.left_panel, Record.get_known_tags())
        self.tagging_text.pack()

        # Requirement
        self.requirement_label = tk.Label(self.right_panel, text="Requirement:")
        self.requirement_label.pack()
        self.requirement_text = tk.Text(self.right_panel)
        self.requirement_text.pack(fill=tk.BOTH, expand=True)

        return tab

    def make_trace_tab(self, master):
        tab = ttk.Frame(master)
        self.connectable_listbox = ttk.Treeview(tab)
        self.connected_listbox = ttk.Treeview(tab)
        #self.move_button = tk.Button(tab, text="Move ->", command=self.move_item)

        self.connectable_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #self.move_button.pack(side=tk.LEFT)
        self.connected_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.connectable_listbox.bind('<ButtonPress-1>', self.on_start)
        self.connectable_listbox.bind('<B1-Motion>', self.on_drag)
        self.connectable_listbox.bind('<ButtonRelease-1>', self.on_drop)

        self.connected_listbox.bind('<ButtonPress-1>', self.on_start)
        self.connected_listbox.bind('<B1-Motion>', self.on_drag)
        self.connected_listbox.bind('<ButtonRelease-1>', self.on_drop)
        return tab

    def on_start(self, event):
        widget = event.widget
        item_id = event.widget.selection()
        record = None
        if widget.winfo_containing(event.x_root, event.y_root) != self.connected_listbox:
            for item in self.connected_listbox.selection():
                self.connected_listbox.selection_remove(item)
        if widget.winfo_containing(event.x_root, event.y_root) != self.connectable_listbox:
            for item in self.connectable_listbox.selection():
                self.connectable_listbox.selection_remove(item)
        if item_id:
            record_item = item_id[0].split("-")
            if record_item[0] == "Req":
                if len(record_item) == 3:
                    record_item[1] = (record_item[1], '')
                record = requirement_list.get_requirement_map()[record_item[1]][int(record_item[2])]

            widget._drag_data = {
                "item": record,
                "parent": widget.winfo_containing(event.x_root, event.y_root)
            }

    def on_drag(self, event):
        widget = event.widget
        widget._drag_data["x"] = event.x
        widget._drag_data["y"] = event.y

    def on_drop(self, event):
        widget = event.widget
        if not hasattr(widget, "_drag_data"):
            return
        if widget._drag_data:
            target_widget = widget.winfo_containing(event.x_root, event.y_root)
            if widget._drag_data["parent"] != self.connected_listbox and target_widget == self.connected_listbox:
                self.connections.append(widget._drag_data["item"])
                self.update_listbox()

    def _add_lists_to_treeview(self, connected, treeview):
        code_list = self.get_list_of_type(connected, Code)
        requirements_list = self.get_list_of_type(connected, Requirement)
        if len(code_list) > 0:
            code_id = treeview.insert("", "end", text="Implementations")
            for x in code_list:
                treeview.insert(code_id, "end", text=x, iid=f"Code-{x.unique_id}")
        if len(requirements_list) > 0:
            requirement_id = treeview.insert("", "end", text="Related Requirements")
            for x in requirements_list:
                treeview.insert(requirement_id, "end", text=x, iid=f"Req-{x.unique_id.to_string()}")

    def get_list_of_type(self, list, _type):
        list_of_type = []
        for x in list:
            if type(x) is _type:
                list_of_type.append(x)
        return list_of_type

    def clear_listboxes(self):
        for item in self.connected_listbox.get_children():
            self.connected_listbox.delete(item)
        for item in self.connectable_listbox.get_children():
            self.connectable_listbox.delete(item)

    def update_listbox(self):
        self.clear_listboxes()
        self.populate_listbox()

    def populate_listbox(self):
        connectable = structures.get_lists()
        connectable = [item for item in connectable if item not in self.connections]
        self._add_lists_to_treeview(self.connections, self.connected_listbox)
        self._add_lists_to_treeview(connectable, self.connectable_listbox)

    def update_combobox_b(self, event=None):
        section = get_variable(self.section)
        if section in requirement_list.get_section_lists():
            b_values = requirement_list.get_subsection_lists(section)
            if b_values:
                self.subsection.update(b_values)

    def create_context_nav(self):
        super().create_context_nav()
        self.add_button = tk.Button(self.context_action_box, text="Add", command=self.add)
        self.add_button.pack(side=tk.LEFT)
        self.cancel_button = tk.Button(self.context_action_box, text="Cancel", command=self.cancel)
        self.cancel_button.pack(side=tk.LEFT)

    def add(self):
        req = Requirement(get_variable(self.section), get_variable(self.subsection), self.title_entry.get(),
                          self.requirement_text.get("1.0", tk.END), self.tagging_text.list)
        requirement_list.append(req)

        page_return()

    def cancel(self):
        page_return()

    def on_hide(self):
        super().on_hide()
        # Reset title entry
        self.title_entry.delete(0, tk.END)
        # Reset subsection combobox
        self.subsection.clear()
        # Reset requirement text
        self.requirement_text.delete("1.0", tk.END)
        # Reset the tags
        self.tagging_text.clear()

    def on_show(self):
        super().on_show()
        # Reset section combobox
        self.section.update(requirement_list.get_section_lists())
        self.tagging_text.update_choices(Record.get_known_tags())
        self.populate_listbox()

    def on_hide(self):
        self.clear_listboxes()

    def on_enter(self, event):
        self.add()
