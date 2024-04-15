from enum import Enum
import tkinter as tk

_current_page = None
_frame_map = dict()
_page_map = dict()
_pages = []
_page_back_stack = [] #For now, Requirement_View is the home page. That will change later.

class PagesEnum(Enum):
    REQUIREMENT_VIEW = 1
    ADD_REQUIREMENTS = 2

def get_enum_from_frame(frame):
    if frame is _frame_map[PagesEnum.REQUIREMENT_VIEW]:
        return PagesEnum.REQUIREMENT_VIEW
    elif frame is _frame_map[PagesEnum.ADD_REQUIREMENTS]:
        return PagesEnum.ADD_REQUIREMENTS


def show_page(page_enum, forgo_stack=False):
    global _current_page, _page_back_stack
    frame = _frame_map[page_enum]
    if frame:
        if _current_page:
            if not forgo_stack:
                _page_back_stack.append(get_enum_from_frame(_current_page))
            _current_page.pack_forget()
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
    page_to_show = _page_back_stack[-1]
    _page_back_stack = _page_back_stack[:-1]
    show_page(page_to_show, forgo_stack=True)

def get_page(page_enum):
    return _page_map[page_enum]


def create_and_register_frame(parent, page_enum, page_type):
    frame = tk.Frame(parent)
    page = page_type(frame)
    page.pack(fill=tk.BOTH, expand=True)
    _frame_map[page_enum] = frame
    _page_map[page_enum] = page
