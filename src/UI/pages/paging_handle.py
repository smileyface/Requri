import logging
from enum import Enum
import tkinter as tk

from src.UI.pages.viewpage import ViewPage


class PagesEnum(Enum):
    RECORD_VIEW = 1
    ADD_REQUIREMENT = 2
    EDIT_REQUIREMENT = 3
    MASS_ADD_REQUIREMENT = 4
    REQUIREMENT_EXTENDED = 5


print("Importing Paging Handle")
_page_map = {}
_initialized = True
_pages = []
_page_back_stack = []  # For now, Requirement_View is the home page. That will change later.
_current_page = None


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
    for enum_key, enum_page in _page_map.items():
        if str(page) == str(enum_page):
            return enum_key
    raise ValueError(f"Unknown page: {page}")


def show_page(page_enum, forgo_stack=False):
    global _current_page
    if page_enum not in _page_map:
        raise KeyError(f"Page {page_enum} not registered")
    new_page = _page_map[page_enum]

    if _current_page:
        _current_page.hide()

        if not forgo_stack:
            _page_back_stack.append(get_enum_from_page(_current_page))

    new_page.pack(expand=True, fill='both')
    new_page.show()
    _current_page = new_page
    logging.debug(f"Page {page_enum} shown successfully.")


def page_return():
    # Don't allow it to go past the home screen
    if len(_page_back_stack) <= 1:
        return
    page_to_show = _page_back_stack.pop()
    show_page(page_to_show, forgo_stack=True)


def get_page(page_enum: Enum) -> ViewPage:
    """
    Get the page object associated with the given page_enum.

    Args:
        page_enum (Enum): The enum value of the page to retrieve.

    Returns:
        tk.Frame: The page object associated with the given page_enum.
    """
    if page_enum in _page_map:
        return _page_map[page_enum]
    else:
        raise KeyError(f"Page enum {page_enum} not found in _page_map")


def get_current_page():
    return get_enum_from_page(_current_page)


def create_and_register_page(parent, page_enum, page_type):
    if parent is None:
        raise KeyError("NoneType")
    if page_enum in _page_map:
        logging.info("Attempting to double add page. Page not added.")
        return
    page = page_type(parent)
    page.create_body()

    parent.update()
    _page_map[page_enum] = page


def clear_paging_handler():
    global _current_page
    _page_map.clear()
    _page_back_stack.clear()
    _current_page = None
