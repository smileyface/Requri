import threading

import pytest
from tests.mocks.mock_main_app import MockMainApplication
import src.UI.pages.paging_handle as PagingHandle
from src.UI.pages.paging_handle import PagesEnum

@pytest.fixture
def app():
    app = MockMainApplication()

    def run_app():
        app.after(0, app.run)

    app_thread = threading.Thread(target=run_app)
    app_thread.start()

    yield app
    app.destroy()
    app_thread.join()

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
