import logging
from enum import Enum
import tkinter as tk

from UI.pages.viewpage import ViewPage


class PagesEnum(Enum):
    RECORD_VIEW = 1
    ADD_REQUIREMENT = 2
    EDIT_REQUIREMENT = 3
    MASS_ADD_REQUIREMENT = 4
    REQUIREMENT_EXTENDED = 5


class PagingHandle:
    _current_page = None
    _page_map = dict()
    _pages = []
    _page_back_stack = []  # For now, Requirement_View is the home page. That will change later.

    @staticmethod
    def get_enum_from_page(page: ViewPage) -> PagesEnum:
        """
        Get the enum value associated with a given frame.

        Args:
            frame (tk.Frame): The frame for which to retrieve the enum value.

        Returns:
            PagesEnum: The enum value associated with the given frame.

        Raises:
            ValueError: If the frame is not found in the _frame_map.

        """
        for enum_key, enum_page in PagingHandle._page_map.items():
            if str(page) == str(enum_page):
                return enum_key
        raise ValueError(f"Unknown page: {page}")

    @staticmethod
    def show_page(page_enum, forgo_stack=False):
        if page_enum not in PagingHandle._page_map:
            raise KeyError(f"Page {page_enum} not registered")
        new_page = PagingHandle._page_map[page_enum]
    
        if PagingHandle._current_page:
            PagingHandle._current_page.hide()

            if not forgo_stack:
                PagingHandle._page_back_stack.append(PagingHandle.get_enum_from_page(PagingHandle._current_page))
                
        new_page.show()
        PagingHandle._current_page = new_page
        logging.debug(f"Page {page_enum} shown successfully.")

    @staticmethod
    def page_return():
        # Don't allow it to go past the home screen
        if len(PagingHandle._page_back_stack) <= 1:
            return
        page_to_show = PagingHandle._page_back_stack.pop()
        PagingHandle.show_page(page_to_show, forgo_stack=True)

    @staticmethod
    def get_page(page_enum: Enum) -> ViewPage:
        """
        Get the page object associated with the given page_enum.

        Args:
            page_enum (Enum): The enum value of the page to retrieve.

        Returns:
            tk.Frame: The page object associated with the given page_enum.
        """
        if page_enum in PagingHandle._page_map:
            return PagingHandle._page_map[page_enum]
        else:
            raise KeyError(f"Page enum {page_enum} not found in _page_map")

    @staticmethod
    def get_current_page():
        return PagingHandle.get_enum_from_page(PagingHandle._current_page)

    @staticmethod
    def create_and_register_page(parent, page_enum, page_type):
        if parent is None:
            raise KeyError("NoneType")
        if page_enum in PagingHandle._page_map:
            logging.info("Attempting to double add page. Page not added.")
            return
        page = page_type(parent)
        page.create_body()

        parent.update()
        PagingHandle._page_map[page_enum] = page

        if PagingHandle._current_page is None:
            PagingHandle.show_page(page_enum, forgo_stack=True)


    @staticmethod
    def clear_paging_handler():
        PagingHandle._page_map.clear()
        PagingHandle._page_back_stack.clear()
        PagingHandle._current_page = None