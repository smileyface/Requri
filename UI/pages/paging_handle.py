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
    def show_page(page_enum: Enum, forgo_stack: bool = False) -> None:
        """
        Display the specified page.

        Args:
            page_enum (Enum): The enum value of the page to display.
            forgo_stack (bool, optional): Whether to forgo adding the current page to the back stack. Defaults to False.

        Raises:
            ValueError: If the specified page_enum is not found in the _page_map.

        Returns:
            None
        """
        logging.info(f"Displaying page {page_enum}")

        frame = PagingHandle.get_page(page_enum)
        if frame:
            if PagingHandle._current_page:
                if not forgo_stack:
                    PagingHandle._page_back_stack.append(PagingHandle.get_enum_from_page(PagingHandle._current_page))
                PagingHandle._current_page.pack_forget()
                PagingHandle._page_map[PagingHandle.get_enum_from_page(PagingHandle._current_page)].on_hide()
            frame.pack(fill=tk.BOTH, expand=True)
            PagingHandle._page_map[page_enum].on_show()
            PagingHandle._current_page = frame
        else:
            raise ValueError(f"Page not found: {page_enum}")

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
        if parent == None:
            raise TypeError("NoneType")
        page = page_type(parent)
        page.create_body()
        PagingHandle._page_map[page_enum] = page

    @staticmethod
    def clear_paging_handler():
        PagingHandle._page_map.clear()
        PagingHandle._page_back_stack.clear()
        PagingHandle._current_page = None