import tkinter as tk
from tkinter import ttk

import pytest

from UI.pages.viewpage import ViewPage


class TestViewPage:

    #  Initialization of ViewPage with a master widget and additional arguments
    def test_initialization_with_master_and_args(self):
        root = tk.Tk()
        view_page = ViewPage(root, "arg1", kwarg1="value1")
        assert view_page.master == root
        assert isinstance(view_page, ViewPage)

    #  Successful retrieval of context_action_box from the master widget
    def test_retrieval_of_context_action_box(self):
        root = tk.Tk()
        root.context_action_box = ttk.Frame(root)
        view_page = ViewPage(root)
        assert view_page.context_action_box == root.context_action_box

    #  Proper packing and display of the page components when show() is called
    def test_show_method(self):
        root = tk.Tk()
        view_page = ViewPage(root)
        view_page.show()
        assert view_page.winfo_ismapped()

    def test_hide_method(self):
        root = tk.Tk()
        view_page = ViewPage(root)
        view_page.show()
        view_page.hide()
        assert not view_page.winfo_ismapped()

    #  Proper destruction of context_action_box children widgets when on_hide() is called
    def test_on_hide_method(self):
        root = tk.Tk()
        context_action_box = ttk.Frame(root)
        context_action_box.pack()
        label = tk.Label(context_action_box, text="Test")
        label.pack()
        root.context_action_box = context_action_box
        view_page = ViewPage(root)
        view_page.on_hide()
        assert len(context_action_box.winfo_children()) == 0

    #  Handling of a master widget without a context_action_box attribute
    def test_no_context_action_box_in_master(self):
        root = tk.Tk()
        view_page = ViewPage(root)
        assert isinstance(view_page.context_action_box, ttk.Frame)

    #  Behavior when create_body, create_context_nav, or display_body methods are not overridden in a subclass
    def test_not_implemented_methods(self):
        root = tk.Tk()
        view_page = ViewPage(root)
        with pytest.raises(NotImplementedError):
            view_page.create_body()
        with pytest.raises(NotImplementedError):
            view_page.create_context_nav()
        with pytest.raises(NotImplementedError):
            view_page.display_body()

    #  Handling of None or invalid master widget during initialization
    def test_invalid_master_widget(self):
        with pytest.raises(AttributeError):
            ViewPage(None)

    #  Behavior when show() is called multiple times consecutively
    def test_multiple_show_calls(self):
        root = tk.Tk()
        view_page = ViewPage(root)
        view_page.show()
        view_page.show()
        assert view_page.winfo_ismapped()

    #  Behavior when hide() is called multiple times consecutively
    def test_multiple_hide_calls(self):
        root = tk.Tk()
        view_page = ViewPage(root)
        view_page.show()
        view_page.hide()
        view_page.hide()
        assert not view_page.winfo_ismapped()

    #  Ensuring that the context_action_box is correctly assigned even if nested within multiple parent widgets
    def test_nested_context_action_box(self):
        root = tk.Tk()
        parent_frame = ttk.Frame(root)
        parent_frame.context_action_box = ttk.Frame(parent_frame)
        nested_frame = ttk.Frame(parent_frame)
        view_page = ViewPage(nested_frame)
        assert view_page.context_action_box == parent_frame.context_action_box

    def test_fallback_context_action_box_creation(self):
        # Setup
        root = tk.Tk()
        parent_frame = tk.Frame(root)
        view_page = ViewPage(parent_frame)

        # Ensure context_action_box is the fallback frame
        assert isinstance(view_page.context_action_box, ttk.Frame)

