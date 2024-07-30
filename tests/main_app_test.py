
from functools import wraps

import pytest

from UI.pages.paging_handle import PagingHandle, PagesEnum
from tests.ui.page.mock_main_app import MockMainApplication


@pytest.fixture
def app():
    app = MockMainApplication()
    yield app
    app.destroy()


@pytest.fixture
def page(app, request):
    if hasattr(request, 'param'):
        page_enum = request.param
        PagingHandle.show_page(page_enum)
        app.update()  # Ensure all widgets are updated
        page = PagingHandle.get_page(page_enum)
    else:
        page = PagingHandle.get_page(PagesEnum.ADD_REQUIREMENT)
    return page


def main_app_test(page_enum):
    def decorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            result = False
            exception = []
            try:
                kwargs['page'] = PagingHandle.get_page(page_enum)
                PagingHandle.show_page(page_enum)
                result = test_func(*args, **kwargs)
            except Exception as e:
                exception.append(e)
            if exception:
                raise exception[0]
            return result
        return wrapper
    return decorator
