import tkinter as tk

class AutoCompleteEntry(tk.Frame):
    """
    AutoCompleteEntry is a custom Tkinter widget that provides an autocomplete
    functionality for entry fields. It allows users to select from a list of
    predefined choices while typing in the entry field.

    Attributes:
        choices (list): List of predefined choices for autocomplete.
        in_state (bool): Indicates whether the widget is in autocomplete state.
        widgetName (str): Name of the widget.
        current_text (str): Current text in the entry field.
        entry (tk.Entry): Tkinter Entry widget for text input.
        option_list (tk.Listbox): Tkinter Listbox widget for displaying choices.

    Methods:
        list (property): Gets or sets the list of entries in the entry field.
        check_trigger(event): Checks for triggers to show or hide the popup.
        backspaces(event): Handles backspace key events.
        show_popup(): Displays the popup listbox with choices.
        _print_popup_state(): Prints the state of the popup (for debugging).
        add_current_text_to_popup(): Adds the current text to the choices list.
        add_choices_from_popup(event): Adds selected choice from the popup to the entry field.
        update_options(): Updates the listbox with filtered choices.
        get_options(): Retrieves the filtered list of choices based on current text.
        update_choices(choices): Updates the predefined choices list.
        insert(index, tag): Inserts a new tag at the specified index in the choices list.
        clear(): Clears the entry field.
    """

    def __init__(self, master, choices, *args, **kwargs):
        """
        Initializes the AutoCompleteEntry widget.

        Parameters:
            master (tk.Widget): Parent widget.
            choices (list): List of predefined choices for autocomplete.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(master, *args, **kwargs)
        self.choices = list(choices)
        self.in_state = False

        self.widgetName = "autocomplete_entry"

        self.current_text = None

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.option_list = tk.Listbox(self, selectmode=tk.SINGLE)

        self.entry.bind('<KeyRelease>', self.check_trigger)
        self.entry.bind('<KeyPress>', self.backspaces)

        self.option_list.bind('<Double-Button-1>', self.add_choices_from_popup)

    @property
    def list(self):
        """
        Gets the list of entries in the entry field.

        Returns:
            list: List of entries in the entry field.
        """
        entries = self.entry.get().split(",")
        for x in range(len(entries)):
            entries[x] = entries[x].strip().strip("#")
        if '' in entries:
            entries.remove('')
        return entries

    @list.setter
    def list(self, value):
        """
        Sets the list of entries in the entry field.

        Parameters:
            value (list): List of entries to set in the entry field.

        Raises:
            ValueError: If the value is not a list.
        """
        if isinstance(value, list):
            self.entry.insert(0, "#" + ", #".join(value) + ",")
        else:
            raise ValueError

    def check_trigger(self, event):
        """
        Checks for triggers to show or hide the popup based on the event keysym.
        If the event keysym is 'numbersign' and the widget is not in autocomplete state,
        it shows the popup. If the event keysym is 'comma' and the popup is visible
        and the widget is in autocomplete state, it adds the current text to the choices
        list and hides the popup. Otherwise, if the widget is in autocomplete state,
        it appends the event character to the current text and updates the options list.

        Parameters:
            event (tk.Event): The key event that triggered this method.
        """
        if event.keysym == 'numbersign' and self.in_state is False:
            self.show_popup()
            self.in_state = True
        elif event.keysym == 'comma' and self.option_list.winfo_ismapped() and self.in_state is True:
            self.add_current_text_to_popup()
            self.in_state = False
        else:
            if self.in_state is True:
                self.current_text += event.char
                self.update_options()

    def backspaces(self, event):
        """
        Handles backspace key events.

        Parameters:
            event (tk.Event): The key event that triggered this method.
        """
        if event.keysym == 'BackSpace':
            current_text = self.entry.get()
            if self.current_text != "" and self.in_state is True:
                self.current_text = self.current_text[:-1]
            elif current_text and current_text[-1] == ",":
                self.in_state = True
                self.show_popup()
                self.current_text = current_text.split("#")[-1][:-1]
            else:
                self.in_state = False
                self.option_list.pack_forget()

    def show_popup(self):
        """
        Displays the popup listbox with choices.
        """
        self.current_text = ""
        if not self.option_list.winfo_ismapped():
            self.update_options()
            self.option_list.pack(fill=tk.BOTH, expand=True)
            self.option_list.update_idletasks()  # Ensure the widget is updated
            self.after(100, self._print_popup_state)  # Add delay to check state

    def _print_popup_state(self):
        """
        Prints the state of the popup (for debugging).
        """
        print("Popup is mapped:", self.option_list.winfo_ismapped())
        print("Popup widget state:", self.option_list)

    def add_current_text_to_popup(self):
        """
        Adds the current text to the choices list.
        """
        self.choices.append(self.current_text)
        self.option_list.pack_forget()

    def add_choices_from_popup(self, event):
        """
        Adds the selected choice from the popup to the entry field.

        Parameters:
            event (tk.Event): The event that triggered this method.
        """
        index = self.option_list.curselection()
        if index:
            selected_text = self.option_list.get(index)
            autocompleted_entry = self.list
            autocompleted_entry.append(selected_text)
            strong = "#" + ", #".join(autocompleted_entry) + ","
            self.entry.delete(0, tk.END)  # Clear existing text
            self.entry.insert(0, strong)  # Insert new text
            self.current_text = selected_text
            self.in_state = False
            self.option_list.pack_forget()

    def update_options(self):
        """
        Updates the listbox with filtered choices.
        """
        self.option_list.delete(0, tk.END)
        choices = self.get_options()
        for choice in choices:
            self.option_list.insert(tk.END, choice)

    def get_options(self):
        """
        Retrieves the filtered list of choices based on current text.

        Returns:
            list: Filtered list of choices.
        """
        options = []
        if self.current_text:
            for choice in self.choices:
                if self.current_text in choice and len(options) < 5:
                    options.append(choice)
        else:
            options = self.choices[:5]
        return options

    def update_choices(self, choices):
        """
        Updates the predefined choices list.

        Parameters:
            choices (list): List of new choices.
        """
        self.choices = choices

    def insert(self, index, tag):
        """
        Inserts a new tag at the specified index in the choices list.

        Parameters:
            index (int): The index at which the tag should be inserted.
            tag (str): The tag to be inserted into the choices list.
        """
        self.choices.insert(index, tag)

    def clear(self):
        """
        Clears the entry field.
        """
        self.entry.delete(0, tk.END)
