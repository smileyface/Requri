import pytest
from testing.mocks.mock_main_app import MockMainApplication
from UI.pages.paging_handle import PagingHandle, PagesEnum

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
