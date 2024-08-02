import tkinter as tk
from tkinter import ttk

import pytest

from UI.pages.viewpage import ViewPage

class TestableViewPage(ViewPage):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.create_body()

    def on_show(self):
        super().on_show()
        # Additional logic for testing

    def on_hide(self):
        super().on_hide()
        # Additional logic for testing

    def display_body(self):
        self.pack(expand=True, fill='both')

    def create_context_nav(self):
        # Example of adding context navigation buttons for testing
        self.add_button = tk.Button(self, text="Add")
        self.add_button.pack()
        self.cancel_button = tk.Button(self, text="Cancel")
        self.cancel_button.pack()

    def create_body(self):
        self.notebook = ttk.Notebook(self, name="test_notebook")
        self.test_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.test_tab, text='Test Tab')
        self.notebook.pack(expand=True, fill='both')


# Fixture to create the testable view page
@pytest.fixture
def test_page(app):
    return TestableViewPage(app)