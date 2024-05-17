from enum import Enum
import tkinter as tk

_current_page = None
_frame_map = dict()
_page_map = dict()
_pages = []
_page_back_stack = []  #For now, Requirement_View is the home page. That will change later.


class PagesEnum(Enum):
    RECORD_VIEW = 1
    ADD_REQUIREMENT = 2
    EDIT_REQUIREMENT = 3
    MASS_ADD_REQUIREMENT = 4
    REQUIREMENT_EXTENDED = 5


def get_enum_from_frame(frame):
    for enum_key, enum_frame in _frame_map.items():
        if frame is enum_frame:
            return enum_key
    raise ValueError("Unknown frame: {}".format(frame))


def show_page(page_enum, forgo_stack=False):
    global _current_page, _page_back_stack
    print(f"Displaying page {page_enum}")
    frame = _frame_map.get(page_enum)
    if frame:
        if _current_page:
            if not forgo_stack:
                _page_back_stack.append(get_enum_from_frame(_current_page))
            _current_page.pack_forget()
            _page_map[get_enum_from_frame(_current_page)].on_hide()
        frame.pack(fill=tk.BOTH, expand=True)
        _page_map[page_enum].on_show()
        _current_page = frame
    else:
        raise ValueError("Page not found")


def page_return():
    global _page_back_stack
    #Don't allow it to go past the home screen
    if len(_page_back_stack) == 0:
        return
    page_to_show = _page_back_stack.pop()
    show_page(page_to_show, forgo_stack=True)


def get_page(page_enum):
    return _page_map[page_enum]


def get_current_page():
    return get_enum_from_frame(_current_page)


def create_and_register_frame(parent, page_enum, page_type):
    frame = tk.Frame(parent)
    page = page_type(frame)
    page.create_body()
    _frame_map[page_enum] = frame
    _page_map[page_enum] = page
