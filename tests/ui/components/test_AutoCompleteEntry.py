# test_show_popup.py

import time
import tkinter as tk

from UI.components.autocomplete_entry import AutoCompleteEntry
from tests.tkinter_test import tkinter_test, root


class TestAutoCompleteEntry:

    @tkinter_test
    def test_entry_field_updates_with_valid_tag(self, root):
        entry = AutoCompleteEntry(root, choices=[])
        entry.pack()
        entry.list = ["tag1"]
        time.sleep(0.2)  # Allow time for UI to update
        return entry.entry.get() == "#tag1,"

    @tkinter_test
    def test_popup_shows_relevant_options_on_hash(self, root):
        entry = AutoCompleteEntry(root, choices=["tag1", "tag2"])
        entry.pack()
        entry.entry.insert(0, "#")
        event = tk.Event()
        event.keysym = 'numbersign'
        entry.check_trigger(event)
        time.sleep(0.2)  # Allow time for the UI to update
        return entry.option_list.winfo_ismapped() == 1

    @tkinter_test
    def test_popup_hides_on_valid_option_selection(self, root):
        entry = AutoCompleteEntry(root, choices=["tag1", "tag2"])
        entry.pack()
        entry.show_popup()
        entry.option_list.selection_set(0)
        entry.add_choices_from_popup(None)
        time.sleep(0.2)  # Allow time for UI to update
        return entry.option_list.winfo_ismapped() == 0

    @tkinter_test
    def test_current_text_added_to_choices_on_comma(self, root):
        entry = AutoCompleteEntry(root, choices=[])
        entry.pack()
        entry.current_text = "newtag"
        event = tk.Event()
        event.keysym = 'comma'
        entry.check_trigger(event)
        time.sleep(0.2)  # Allow time for UI to update
        return "newtag" in entry.choices

    @tkinter_test
    def test_entry_field_updates_on_double_click(self, root):
        entry = AutoCompleteEntry(root, choices=["tag1", "tag2"])
        entry.pack()
        entry.show_popup()
        entry.option_list.selection_set(0)
        entry.add_choices_from_popup(None)
        time.sleep(0.2)  # Allow time for UI to update
        return "#tag1," in entry.entry.get()

    @tkinter_test
    def test_choices_list_updates_correctly(self, root):
        entry = AutoCompleteEntry(root, choices=["tag1"])
        entry.pack()
        new_choices = ["newtag1", "newtag2"]
        entry.update_choices(new_choices)
        time.sleep(0.2)  # Allow time for UI to update
        return entry.choices == new_choices

    @tkinter_test
    def test_entry_field_handles_empty_input(self, root):
        entry = AutoCompleteEntry(root, choices=[])
        entry.pack()
        entry.entry.insert(0, "")
        time.sleep(0.2)  # Allow time for UI to update
        return entry.entry.get() == ""

    @tkinter_test
    def test_entry_field_handles_special_characters(self, root):
        entry = AutoCompleteEntry(root, choices=[])
        entry.pack()
        special_chars = "!@#$%^&*()"
        entry.entry.insert(0, special_chars)
        time.sleep(0.2)  # Allow time for UI to update
        return entry.entry.get() == special_chars

    @tkinter_test
    def test_entry_field_handles_rapid_key_presses(self, root):
        entry = AutoCompleteEntry(root, choices=["tag1", "tag2"])
        entry.pack()
        for char in "rapidinput":
            event = tk.Event()
            event.char = char
            event.keysym = char
            entry.check_trigger(event)
        time.sleep(0.2)  # Allow time for UI to update
        return True  # If no error occurs, the test passes

    @tkinter_test
    def test_entry_field_handles_backspace_with_no_text(self, root):
        entry = AutoCompleteEntry(root, choices=[])
        entry.pack()
        event = tk.Event()
        event.keysym = 'BackSpace'
        entry.backspaces(event)
        time.sleep(0.2)  # Allow time for UI to update
        return True  # If no error occurs, the test passes

    @tkinter_test
    def test_entry_field_handles_long_input(self, root):
        entry = AutoCompleteEntry(root, choices=[])
        entry.pack()
        long_input = "a" * 1000
        entry.entry.insert(0, long_input)
        time.sleep(0.2)  # Allow time for UI to update
        return entry.entry.get() == long_input

    @tkinter_test
    def test_entry_field_clears_correctly(self, root):
        entry = AutoCompleteEntry(root, choices=[])
        entry.pack()
        entry.entry.insert(0, "sometext")
        entry.clear()
        time.sleep(0.2)  # Allow time for UI to update
        return entry.entry.get() == ""

    @tkinter_test
    def test_show_popup(self, root):
        entry = AutoCompleteEntry(root, choices=["tag1", "tag2"])
        entry.pack()
        entry.show_popup()
        time.sleep(0.2)  # Allow time for the UI to update
        return entry.option_list.winfo_ismapped() == 1

    @tkinter_test
    def test_empty_choices_list(self, root):
        entry = AutoCompleteEntry(root, choices=[])
        entry.pack()
        entry.entry.insert(0, "#")
        event = tk.Event()
        event.keysym = 'numbersign'
        entry.check_trigger(event)
        time.sleep(0.2)  # Allow time for UI to update
        return entry.option_list.size() == 0  # Ensure the listbox is empty

    @tkinter_test
    def test_partial_matches(self, root):
        entry = AutoCompleteEntry(root, choices=["tag1", "tag2", "other"])
        entry.pack()
        entry.entry.insert(0, "#ta")
        event = tk.Event()
        event.keysym = 'a'
        entry.check_trigger(event)
        time.sleep(0.2)  # Allow time for UI to update
        return entry.option_list.size() == 2  # Ensure only "tag1" and "tag2" are shown

    @tkinter_test
    def test_case_insensitivity(self, root):
        entry = AutoCompleteEntry(root, choices=["Tag1", "tag2", "TAG3"])
        entry.pack()
        entry.entry.insert(0, "#t")
        event = tk.Event()
        event.keysym = 't'
        entry.check_trigger(event)
        time.sleep(0.2)  # Allow time for UI to update
        return entry.option_list.size() == 3  # Ensure all variations of "t" are shown

    @tkinter_test
    def test_non_alphanumeric_characters(self, root):
        entry = AutoCompleteEntry(root, choices=["@tag1", "#tag2", "$tag3"])
        entry.pack()
        entry.entry.insert(0, "#")
        event = tk.Event()
        event.keysym = 'numbersign'
        entry.check_trigger(event)
        time.sleep(0.2)  # Allow time for UI to update
        return entry.option_list.size() == 1  # Ensure only "#tag2" is shown

    @tkinter_test
    def test_focus_out_behavior(self, root):
        entry = AutoCompleteEntry(root, choices=["tag1", "tag2"])
        entry.pack()
        entry.entry.insert(0, "#ta")
        entry.show_popup()
        time.sleep(0.2)  # Allow time for UI to update
        entry.entry.event_generate("<FocusOut>")  # Simulate focus out
        time.sleep(0.2)  # Allow time for UI to update
        return entry.option_list.winfo_ismapped() == 0  # Ensure the popup hides

    @tkinter_test
    def test_click_outside_behavior(self, root):
        entry = AutoCompleteEntry(root, choices=["tag1", "tag2"])
        entry.pack()
        entry.entry.insert(0, "#ta")
        entry.show_popup()
        time.sleep(0.2)  # Allow time for UI to update
        entry.event_generate("<Button-1>", x=0, y=0)  # Simulate click outside
        time.sleep(0.2)  # Allow time for UI to update
        return entry.option_list.winfo_ismapped() == 0  # Ensure the popup hides

    @tkinter_test
    def test_listbox_scroll(self, root):
        entry = AutoCompleteEntry(root, choices=[f"tag{i}" for i in range(20)])
        entry.pack()
        entry.entry.insert(0, "#")
        event = tk.Event()
        event.keysym = 'numbersign'
        entry.check_trigger(event)
        time.sleep(0.2)  # Allow time for UI to update
        return entry.option_list.yview()  # Ensure the listbox can be scrolled

    @tkinter_test
    def test_keyboard_navigation(self, root):
        entry = AutoCompleteEntry(root, choices=["tag1", "tag2", "tag3"])
        entry.pack()
        entry.entry.insert(0, "#")
        entry.show_popup()
        time.sleep(0.2)  # Allow time for UI to update
        event = tk.Event()
        event.keysym = 'Down'
        entry.option_list.event_generate("<KeyPress-Down>")  # Simulate down arrow key press
        time.sleep(0.2)  # Allow time for UI to update
        return entry.option_list.curselection() == (0,)  # Ensure the first item is selected

    @tkinter_test
    def test_selection_persistence(self, root):
        entry = AutoCompleteEntry(root, choices=["tag1", "tag2"])
        entry.pack()
        entry.entry.insert(0, "#")
        entry.show_popup()
        entry.option_list.selection_set(0)
        entry.add_choices_from_popup(None)
        entry.entry.insert(tk.END, " more text")
        return entry.entry.get() == "#tag1, more text"  # Ensure the selection persists