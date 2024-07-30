import tkinter as tk
from enum import Enum

# Generated by CodiumAI

from UI.pages.paging_handle import PagingHandle, PagesEnum

import pytest

from UI.pages.viewpage import ViewPage
from tests.tkinter_test import tkinter_test, root


class TestPage(ViewPage):
    def __init__(self, master):
        self.create_body_called = False
        super().__init__(master)

    def create_body(self) -> None:
        self.create_body_called = True

    def create_context_nav(self) -> None:
        pass

    def display_body(self):
        pass

    def on_show(self):
        pass

    def on_hide(self):
        pass


class TestPagingHandle:

    
    @pytest.fixture(autouse=True)
    def teardown(self):
        yield
        PagingHandle.clear_paging_handler()

    #  show_page displays the correct frame for the given enum
    @tkinter_test
    def test_show_page_displays_correct_frame(self, root):
        PagingHandle.create_and_register_page(root, PagesEnum.RECORD_VIEW, TestPage)
        PagingHandle.show_page(PagesEnum.RECORD_VIEW)
        assert PagingHandle._current_page == PagingHandle.get_page(PagesEnum.RECORD_VIEW)

    #  show_page adds the current page to the back stack if forgo_stack is False
    @tkinter_test
    def test_show_page_adds_to_back_stack(self, root):
        PagingHandle.create_and_register_page(root, PagesEnum.RECORD_VIEW, TestPage)
        PagingHandle.create_and_register_page(root, PagesEnum.ADD_REQUIREMENT, TestPage)
        #Record_View is already shown
        PagingHandle.show_page(PagesEnum.ADD_REQUIREMENT)
        assert PagingHandle._page_back_stack == [PagesEnum.RECORD_VIEW]

    #  get_page returns the correct page object for the given enum
    @tkinter_test
    def test_get_page_returns_correct_object(self, root):
        PagingHandle.create_and_register_page(root, PagesEnum.RECORD_VIEW, TestPage)
        page = PagingHandle.get_page(PagesEnum.RECORD_VIEW)
        assert isinstance(page, TestPage)

    #  get_current_page returns the enum of the currently displayed page
    @tkinter_test
    def test_get_current_page_returns_enum(self, root):
        PagingHandle.create_and_register_page(root, PagesEnum.RECORD_VIEW, TestPage)
        PagingHandle.show_page(PagesEnum.RECORD_VIEW)
        current_page_enum = PagingHandle.get_current_page()
        assert current_page_enum == PagesEnum.RECORD_VIEW

    #  create_and_register_page correctly creates and registers a frame and its associated page
    @tkinter_test
    def test_create_and_register_frame_creates_and_registers_correctly(self, root):
        PagingHandle.create_and_register_page(root, PagesEnum.RECORD_VIEW, TestPage)
        assert isinstance(PagingHandle._page_map[PagesEnum.RECORD_VIEW], TestPage)

    #  create_and_register_page calls create_body on the page object
    @tkinter_test
    def test_create_and_register_frame_calls_create_body(self, root):

        PagingHandle.create_and_register_page(root, PagesEnum.RECORD_VIEW, TestPage)
        assert PagingHandle._page_map[PagesEnum.RECORD_VIEW].create_body_called is True

    #  show_page does not add the current page to the back stack if forgo_stack is True
    @tkinter_test
    def test_show_page_does_not_add_to_back_stack_if_forgo_stack_true(self, root):
        PagingHandle.create_and_register_page(root, PagesEnum.RECORD_VIEW, TestPage)
        PagingHandle.create_and_register_page(root, PagesEnum.ADD_REQUIREMENT, TestPage)
        PagingHandle.show_page(PagesEnum.RECORD_VIEW)
        PagingHandle.show_page(PagesEnum.ADD_REQUIREMENT, forgo_stack=True)
        assert PagingHandle._page_back_stack == [PagesEnum.RECORD_VIEW]

    #  show_page raises ValueError if the page_enum is not found in _page_map
    def test_show_page_raises_value_error_for_invalid_enum(self):
        class InvalidEnum(Enum):
            INVALID_PAGE = 99

        with pytest.raises(KeyError):
            PagingHandle.show_page(InvalidEnum.INVALID_PAGE)

    #  get_enum_from_page raises ValueError if the frame is not found in _frame_map
    def test_get_enum_from_frame_raises_value_error_for_invalid_frame(sel):
        invalid_frame = tk.Frame()

        with pytest.raises(ValueError) as excinfo:
            PagingHandle.get_enum_from_page(invalid_frame)

        assert "Unknown page" in str(excinfo.value)

    #  page_return does nothing if the back stack is empty
    def test_page_return_does_nothing_if_back_stack_empty(self):
        initial_back_stack_length = len(PagingHandle._page_back_stack)

        PagingHandle.page_return()

        assert len(PagingHandle._page_back_stack) == initial_back_stack_length

    #  show_page handles cases where _current_page is None
    @tkinter_test
    def test_show_page_handles_none_current_page(self, root):
        PagingHandle.create_and_register_page(root, PagesEnum.RECORD_VIEW, TestPage)

        # Ensure _current_page is None initially
        PagingHandle._current_page = None

        # Show page and check if it handles None _current_page correctly
        PagingHandle.show_page(PagesEnum.RECORD_VIEW)

        assert PagingHandle._current_page == PagingHandle.get_page(PagesEnum.RECORD_VIEW)

    #  create_and_register_page handles cases where parent is Non
    def test_create_and_register_frame_handles_none_parent(self):
        with pytest.raises(KeyError) as excinfo:
            PagingHandle.create_and_register_page(None, PagesEnum.RECORD_VIEW, TestPage)

        assert "NoneType" in str(excinfo.value)

    #  clear_paging_handler resets all internal states of PagingHandle
    @tkinter_test
    def test_clear_paging_handler_resets_states(self, root):
        # Setup
        PagingHandle.create_and_register_page(root, PagesEnum.RECORD_VIEW, TestPage)
        PagingHandle.create_and_register_page(root, PagesEnum.ADD_REQUIREMENT, TestPage)
        PagingHandle.show_page(PagesEnum.RECORD_VIEW)
        PagingHandle.show_page(PagesEnum.ADD_REQUIREMENT)

        # Ensure initial state
        assert len(PagingHandle._page_map) == 2
        assert len(PagingHandle._page_back_stack) == 2
        assert PagingHandle._current_page is not None

        # Call clear_paging_handler
        PagingHandle.clear_paging_handler()

        # Check if states are reset
        assert len(PagingHandle._page_map) == 0
        assert len(PagingHandle._page_back_stack) == 0
        assert PagingHandle._current_page is None

    #  page_return does not allow navigation past the home screen
    @tkinter_test
    def test_page_return_does_not_allow_navigation_past_home_screen(self, root):
        PagingHandle.create_and_register_page(root, PagesEnum.RECORD_VIEW, TestPage)
        PagingHandle.create_and_register_page(root, PagesEnum.ADD_REQUIREMENT, TestPage)
        PagingHandle.show_page(PagesEnum.RECORD_VIEW)
        PagingHandle.show_page(PagesEnum.ADD_REQUIREMENT)
        initial_back_stack_length = len(PagingHandle._page_back_stack)

        # Try to navigate past the home screen
        PagingHandle.page_return()

        # Check if back stack remains the same
        assert len(PagingHandle._page_back_stack) == 1

    # Test: Ensure only one page is visible at a time
    @tkinter_test
    def test_only_one_page_visible_at_a_time(self, root):
        PagingHandle.create_and_register_page(root, PagesEnum.RECORD_VIEW, TestPage)
        PagingHandle.create_and_register_page(root, PagesEnum.ADD_REQUIREMENT, TestPage)

        # Show RECORD_VIEW page
        PagingHandle.show_page(PagesEnum.RECORD_VIEW)
        root.update()

        record_view_page = PagingHandle.get_page(PagesEnum.RECORD_VIEW)
        add_requirement_page = PagingHandle.get_page(PagesEnum.ADD_REQUIREMENT)

        assert record_view_page.winfo_viewable() == 1
        assert add_requirement_page.winfo_viewable() == 0

        # Show ADD_REQUIREMENT page
        PagingHandle.show_page(PagesEnum.ADD_REQUIREMENT)
        root.update()

        assert record_view_page.winfo_viewable() == 0
        assert add_requirement_page.winfo_viewable() == 1