import re
import logging
import tkinter as tk
from tkinter import ttk
from typing import List, Union, Any

from UI.components.autocomplete_entry import AutoCompleteEntry
from UI.components.combobox_with_add import ComboboxWithAdd
from UI.pages.paging_handle import PagingHandle
from UI.pages.viewpage import ViewPage
from structures.lists import requirement_list
from structures.records import *
from structures.records.record import Record


def get_variable(var):
    if var is not None and var.variable is not None:
        return re.sub(r"'", '', var.variable.get())
    return None


class AddRequirementPage(ViewPage):
    """
    AddRequirementPage is a GUI component that allows users to add and manage requirements.
    It provides input fields for requirement details, tag management, and a traceability feature
    to connect related items.

    Attributes:
        cancel_button (tk.Button): Button to cancel the operation.
        add_button (tk.Button): Button to add a new requirement.
        requirement_text (tk.Text): Text widget for entering the requirement description.
        requirement_label (tk.Label): Label for the requirement text.
        tagging_text (AutoCompleteEntry): Autocomplete entry for tags.
        tagging_label (tk.Label): Label for the tagging text.
        subsection (ComboboxWithAdd): Combobox for selecting the subsection.
        subsection_label (tk.Label): Label for the subsection combobox.
        section (ComboboxWithAdd): Combobox for selecting the section.
        section_label (tk.Label): Label for the section combobox.
        title_entry (tk.Entry): Entry widget for the requirement title.
        title_label (tk.Label): Label for the title entry.
        right_panel (tk.Frame): Frame for the right panel.
        left_panel (tk.Frame): Frame for the left panel.
        connected_listbox (ttk.Treeview): Treeview for displaying connected items.
        connectable_listbox (ttk.Treeview): Treeview for displaying connectable items.
        connections (list): List of connected items.
    """

    def __init__(self, parent_widget, *args: Any, **kwargs: Any):
        """
        Initializes the AddRequirementPage.

        Parameters:
            parent_widget (tk.Widget): The parent widget.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(parent_widget, *args, **kwargs)
        self._drag_data = None
        self.requirement_tab = None
        self.trace_tab = None
        self.notebook = None
        self.cancel_button = None
        self.add_button = None
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
        self.connected_listbox = None
        self.connectable_listbox = None
        self.connections = []
        self._initialize_drag_data()

    def _initialize_drag_data(self):
        self._drag_data = {"x": 0, "y": 0, "item": None, "parent": None}

    def create_label_and_entry(self, parent, label_text, entry_type=tk.Entry):
        label = tk.Label(parent, text=label_text)
        entry = entry_type(parent)
        return label, entry

    def on_drop(self, event: tk.Event) -> None:
        """
        Handles the drop event for drag-and-drop functionality.

        Parameters:
            event (tk.Event): The event object containing drop details.
        """
        try:
            widget = event.widget
            if self._drag_data["item"]:
                target_widget = widget.winfo_containing(event.x_root, event.y_root)
                if target_widget == self.connected_listbox:
                    item_id = self._drag_data["item"]
                    if item_id and item_id not in self.connections:
                        self.connections.append(item_id)
                        self.update_listbox()
            self._initialize_drag_data()
        except Exception as e:
            logging.error(f"Error in on_drop method: {e}")

    def on_select(self, event):
        """
        Handles the selection event for treeview items.

        Parameters:
            event (tk.Event): The event object containing selection details.
        """
        selected_item = event.widget.selection()
        if selected_item:
            item = event.widget.item(selected_item)
            logging.info(f"Selected item: {item['text']}")

    def on_drag(self, event: tk.Event) -> None:
        """
        Handles the drag event for drag-and-drop functionality.

        Parameters:
            event (tk.Event): The event object containing drag details.
        """
        try:
            widget = event.widget
            if self._drag_data["item"] is None:
                self._drag_data = {"x": event.x_root, "y": event.y_root, "item": widget.selection(), "parent": widget}
            else:
                dx = event.x - self._drag_data["x"]
                dy = event.y - self._drag_data["y"]
                widget.move(self._drag_data["item"], dx, dy)
        except Exception as e:
            logging.error(f"Error in on_drag method: {e}")

    def get_list_of_type(self, input_list: List[Any], _type: type) -> List[Any]:
        """
        Filter a list based on a specific type.

        Args:
            input_list (list): The input list to filter.
            _type (type): The type to filter the list with.

        Returns:
            list: A filtered list containing only elements of the specified type.
        """
        if not isinstance(_type, type):
            raise TypeError("`_type` must be a valid type")
        return [x for x in input_list if isinstance(x, _type)]

    def _add_lists_to_treeview(self, connected: List[Union[Code, Requirement]], treeview: ttk.Treeview) -> None:
        """
        Adds lists of connected items to the treeview.

        Parameters:
            connected (list): List of connected Code and Requirement objects.
            treeview (ttk.Treeview): The treeview to update.
        """
        code_list = self.get_list_of_type(connected, Code)
        requirements_list = self.get_list_of_type(connected, Requirement)

        for item_list, item_type, item_text, item_prefix in [
            (requirements_list, "Requirement", "Related Requirements", "Req-"),
            (code_list, "Code", "Implementations", "Code-")]:
            for item in item_list:
                item_id = treeview.insert("", "end", text=item_text)
                try:
                    if item.unique_id is None:
                        logging.error(f"{item_type} item has no unique_id: {item}")
                        continue  # Skip items with None unique_id
                    treeview.insert(item_id, "end", text=item, iid=f"{item_prefix}{str(item.unique_id)}")
                except Exception as e:
                    logging.error(f"Error inserting {item_type} item: {e}")
                    raise e

    def create_body(self):
        """
        Creates the main body of the AddRequirementPage, including tabs for requirement input and traceability.
        """
        super().create_body()

        self.notebook = ttk.Notebook(self, name="add_requirement_body")

        self.requirement_tab = self.make_requirement_tab(self.notebook)
        self.trace_tab = self.make_trace_tab(self.notebook)

        self.notebook.add(self.requirement_tab, text='Add Requirement')
        self.notebook.add(self.trace_tab, text='Traceability')

    def display_body(self):
        self.pack(expand=True, fill='both')
        self.notebook.pack(expand=True, fill='both')
        # Requirements Tab
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.section_label.pack()
        self.section.pack()
        self.subsection_label.pack()
        self.subsection.pack()
        self.tagging_label.pack()
        self.tagging_text.pack()
        self.requirement_label.pack()
        self.requirement_text.pack()

        # Trace Tab
        self.connectable_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.connected_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def make_trace_tab(self, root):
        """
        Creates the traceability tab for the notebook.

        Returns:
            ttk.Frame: The created traceability tab.
        """
        tab = ttk.Frame(root, name="add_requirements_trace_tab")
        self.connectable_listbox = ttk.Treeview(tab)
        self.connected_listbox = ttk.Treeview(tab)

        self.bind_treeview_events(self.connectable_listbox)
        self.bind_treeview_events(self.connected_listbox)

        return tab

    def bind_treeview_events(self, treeview):
        treeview.bind('<<TreeviewSelect>>', self.on_select)
        treeview.bind('<B1-Motion>', self.on_drag)
        treeview.bind('<ButtonRelease-1>', self.on_drop)

    def make_requirement_tab(self, root):
        """
        Creates the requirement tab for the notebook.

        Returns:
            ttk.Frame: The created requirement tab.
        """
        tab = ttk.Frame(root, name="add_requirements_req_tab")

        # Create left panel for inputs
        self.left_panel = tk.Frame(tab, name="left_requirements_panel")

        # Create right panel for text block
        self.right_panel = tk.Frame(tab, name="right_requirements_panel")

        # Title
        self.title_label, self.title_entry = self.create_label_and_entry(self.left_panel, "Title:")

        # Section
        self.section_label, self.section = self.create_label_and_entry(self.left_panel, "Section:", ComboboxWithAdd)
        self.section.configure(values=requirement_list.get_section_lists(), selected_callback=self.update_combobox_b)

        # Subsection
        self.subsection_label, self.subsection = self.create_label_and_entry(self.left_panel, "Subsection:",
                                                                             ComboboxWithAdd)
        self.subsection.configure(values=requirement_list.get_subsection_lists(self.section))

        # Tags
        self.tagging_label, self.tagging_text = self.create_label_and_entry(self.left_panel, "Tags:", AutoCompleteEntry)
        self.tagging_text.configure(choices=Record.get_known_tags())

        # Requirement
        self.requirement_label, self.requirement_text = self.create_label_and_entry(self.right_panel, "Requirement:",
                                                                                    tk.Text)

        return tab

    def update_combobox_b(self, event=None):
        """
        Updates the subsection combobox based on the selected section.

        Parameters:
            event (tk.Event, optional): The event that triggered this method.
        """
        section = get_variable(self.section)
        if section in requirement_list.get_section_lists():
            b_values = requirement_list.get_subsection_lists(section)
            for x in b_values:
                self.subsection.add_value(x)

    def update_listbox(self):
        """
        Updates the connected listbox with the current connections.
        """
        # Clear the current items in the connected listbox
        for item in self.connected_listbox.get_children():
            self.connected_listbox.delete(item)

        # Add the updated connections to the connected listbox
        self._add_lists_to_treeview(self.connections, self.connected_listbox)

    def create_context_nav(self) -> None:
        """
        Creates the context navigation buttons for adding and canceling operations.
        """
        self.add_button = tk.Button(self.context_action_box, text="Add", command=self.add)
        self.add_button.pack(anchor="s")
        self.cancel_button = tk.Button(self.context_action_box, text="Cancel", command=self.cancel)
        self.cancel_button.pack(anchor="s")

    def is_duplicate(self, req):
        for existing_req in requirement_list.get_requirement_list():
            if (existing_req.title == req.title and
                    existing_req.section == req.section and
                    existing_req.sub == req.sub and
                    existing_req.text == req.text):
                return True
        return False

    def is_empty(self, req):
        return req.title == "" and req.section == "" and req.sub == "" and req.text == ""

    def add(self):
        section = get_variable(self.section)
        subsection = get_variable(self.subsection)
        if self.title_entry:
            title = self.title_entry.get()
        else:
            title = None
        if self.requirement_text:
            requirement_text = self.requirement_text.get("1.0", tk.END)
        else:
            requirement_text = ""
        tags = self.tagging_text.list if self.tagging_text else []

        if None in (section, subsection, title, requirement_text):
            logging.error("Missing required information. Cannot add the requirement.")
            return

        req = Requirement(section, subsection, title, requirement_text, tags)

        if self.is_duplicate(req):
            logging.info("Duplicate requirement. Not adding to the list.")
            return
        if self.is_empty(req):
            logging.info("Requirement is empty. Not adding to the list.")
            return

        requirement_list.append(req)

    def cancel(self):
        """
        Cancels the operation and navigates back to the previous page.
        """
        PagingHandle.page_return()
