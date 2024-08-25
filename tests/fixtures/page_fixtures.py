import pytest

from src.UI.pages.requirements.add_requirement import AddRequirementPage
from src.UI.pages.requirements.edit_requirement import EditRequirementPage
import src.UI.pages.paging_handle as PagingHandle
from src.structures.lists import requirement_list
from tests.mocks.mock_main_app import MockMainApplication


def create_and_show_page(page_class: PagingHandle.PagesEnum, requirement=None):
    if requirement:
        PagingHandle.get_page(page_class).requirement = requirement
    PagingHandle.show_page(page_class)
    return PagingHandle.get_page(page_class)


@pytest.fixture
def edit_requirement_page(app, request):
    requirement = request.param
    requirement_list.append(requirement)
    page = create_and_show_page(PagingHandle.PagesEnum.EDIT_REQUIREMENT
                                , requirement)
    app.update_idletasks()
    yield page


@pytest.fixture
def add_requirement_page(app):
    page = create_and_show_page(PagingHandle.PagesEnum.ADD_REQUIREMENT)
    app.update_idletasks()
    yield page
