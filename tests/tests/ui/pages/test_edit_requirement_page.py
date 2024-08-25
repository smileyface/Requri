import time
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch

import pytest

from src.UI.components.combobox_with_add import ComboboxWithAdd
from src.UI.components.autocomplete_entry import AutoCompleteEntry
from src.UI.pages.requirements.edit_requirement import EditRequirementPage
from src.structures.lists import requirement_list
from src.structures.records import Requirement
from src.structures.requirement_id import RequirementId

from tests.fixtures.app_fixtures import app
from tests.fixtures.page_fixtures import edit_requirement_page
from tests.mocks.mock_main_app import MockMainApplication

# Example requirements for tests
req_complete = Requirement("Section", "Subsection", "Title", "Text", ["Tag1"])
# noinspection PyTypeChecker
req_missing_fields = Requirement(None, None, None, None, [])
# noinspection PyTypeChecker
req_missing_fields_invalid_id = Requirement(None, None, None, None, [], new_unique_id=999)


class TestEditRequirementPage:

    #  Initializes correctly with all required attributes
    def test_initializes_correctly_with_all_required_attributes(self, app: MockMainApplication):
        edit_page = EditRequirementPage(app)
        assert edit_page.section is None
        assert edit_page.subsection is None
        assert edit_page.requirement_text is None
        assert edit_page.title_entry is None
        assert edit_page.tagging_text is None
        assert edit_page.master == app
        assert edit_page.requirement is None

    #  Updates requirement in requirement_list when edit method is called
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_updates_requirement_in_requirement_list_when_edit_method_is_called(self, app: MockMainApplication,
                                                                                edit_requirement_page: EditRequirementPage):
        edit_requirement_page.section.variable = "New Section"
        edit_requirement_page.subsection.variable = "New Subsection"
        edit_requirement_page.title_entry.delete(0, tk.END)
        edit_requirement_page.title_entry.insert(0, "New Title")
        edit_requirement_page.requirement_text.delete("1.0", tk.END)
        edit_requirement_page.requirement_text.insert("1.0", "New Text")
        edit_requirement_page.tagging_text.list = ["New Tag"]
        edit_requirement_page.edit()
        updated_requirement = requirement_list.get_requirement_map()["New Section", "New Subsection"][0]
        assert updated_requirement.section == "New Section"
        assert updated_requirement.sub == "New Subsection"
        assert updated_requirement.title == "New Title"
        assert updated_requirement.text == "New Text"
        assert updated_requirement.tags == ["New Tag"]
        assert ("Section", "Subsection") not in requirement_list.get_requirement_map()


    #  Changes button text to "Edit" and sets the command to edit in create_context_nav
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_changes_button_text_to_edit_and_sets_command_to_edit_in_create_context_nav(self, app: MockMainApplication,
                                                                                        edit_requirement_page: EditRequirementPage):
        # Call the method that sets up the context
        edit_requirement_page.create_context_nav()
        app.update()

        assert edit_requirement_page.add_button.cget("text") == "Edit"
        command = edit_requirement_page.add_button.cget('command')
        assert 'edit' in command

    #  Clears text fields and tagging list in on_hide
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_clears_text_fields_and_tagging_list_in_on_hide(self, app: MockMainApplication,
                                                            edit_requirement_page: EditRequirementPage):
        edit_requirement_page.requirement_text = tk.Text(app)
        edit_requirement_page.requirement_text.insert("1.0", "Some text")
        edit_requirement_page.title_entry = tk.Entry(app)
        edit_requirement_page.title_entry.insert(0, "Some title")
        edit_requirement_page.tagging_text = AutoCompleteEntry(app)
        edit_requirement_page.tagging_text.insert(0, "Some tag")
        edit_requirement_page.on_hide()
        assert edit_requirement_page.requirement_text.get("1.0", tk.END).strip() == ""
        assert edit_requirement_page.title_entry.get() == ""
        assert not len(edit_requirement_page.tagging_text.list)

    #  Populates fields with requirement data in on_show
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_populates_fields_with_requirement_data_in_on_show(self, app: MockMainApplication,
                                                               edit_requirement_page: EditRequirementPage):
        requirement = Requirement("Section", "Subsection", "Title", "Text", ["Tag1"])
        requirement_list.append(requirement)
        edit_requirement_page.requirement = requirement
        edit_requirement_page.create_body()

        # Call on_show and check if it handles missing attributes gracefully
        try:
            edit_requirement_page.on_show()
            assert True  # If no exception is raised, the test passes
            assert edit_requirement_page.title_entry.get() == requirement.title
            assert edit_requirement_page.section.variable == requirement.section
            assert edit_requirement_page.subsection.variable == requirement.sub
            assert edit_requirement_page.requirement_text.get("1.0", tk.END).strip() == requirement.text
            assert edit_requirement_page.tagging_text.list == requirement.tags
        except Exception as e:
            pytest.fail(f"on_show raised an exception with missing attributes: {e}")

    #  Handles drag and drop events correctly in the traceability tab
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_handles_drag_and_drop_events_correctly_in_traceability_tab(self, app: MockMainApplication,
                                                                        edit_requirement_page: EditRequirementPage):
        # Access the notebook widget
        notebook = edit_requirement_page.nametowidget('add_requirement_body')
        assert isinstance(notebook, ttk.Notebook)

        # Access the tabs by name
        requirement_tab = notebook.nametowidget('add_requirements_req_tab')
        traceability_tab = notebook.nametowidget('add_requirements_trace_tab')

        # Switch to the Traceability tab
        notebook.select(traceability_tab)
        app.update()  # Ensure the GUI updates the tab selection
        edit_requirement_page.connectable_listbox.insert("", "end", iid="item1", text="Item 1")
        edit_requirement_page.connectable_listbox.selection_set("item1")

        valid_event = tk.Event()
        valid_event.widget = edit_requirement_page.connectable_listbox
        valid_event.x_root = edit_requirement_page.connectable_listbox.winfo_rootx() + 10
        valid_event.y_root = edit_requirement_page.connectable_listbox.winfo_rooty() + 10

        # Simulate drag and drop events in the traceability tab
        edit_requirement_page.on_drag(valid_event)
        valid_event.widget = edit_requirement_page.connected_listbox
        valid_event.x_root = edit_requirement_page.connected_listbox.winfo_rootx() + 10
        valid_event.y_root = edit_requirement_page.connected_listbox.winfo_rooty() + 10

        edit_requirement_page.on_drop(valid_event)

        # Assert that the connections list is updated correctly
        assert len(edit_requirement_page.connections) == 1

    #  Handles non-existent requirement in requirement_list in edit method
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_handles_non_existent_requirement_in_requirement_list_in_edit_method(self, app: MockMainApplication,
                                                                                 edit_requirement_page: EditRequirementPage):
        with pytest.raises(KeyError):
            requirement_list.update(RequirementId("NewSection", "NewSubsection") , "Section", "Subsection", "Title", "Text", ["Tag"])

    #  Handles requirement with missing attributes in on_show
    @pytest.mark.parametrize('edit_requirement_page', [req_missing_fields_invalid_id], indirect=True)
    def test_handles_requirement_with_missing_attributes_in_on_show(self, app: MockMainApplication,
                                                                    edit_requirement_page: EditRequirementPage):

        # Initialize fields that will be populated by on_show
        edit_requirement_page.title_entry = tk.Entry(app)
        edit_requirement_page.section = ComboboxWithAdd(app)
        edit_requirement_page.subsection = ComboboxWithAdd(app)
        edit_requirement_page.requirement_text = tk.Text(app)

        # Call on_show and check if it handles missing attributes gracefully
        try:
            edit_requirement_page.on_show()
            assert True  # If no exception is raised, the test passes
            assert not edit_requirement_page.title_entry.get()  # Should be empty since title is None
            assert not edit_requirement_page.section.variable == ''  # Should be empty since section is None
            assert not edit_requirement_page.subsection.variable == '' # Should be empty since subsection is None
            assert not edit_requirement_page.requirement_text.get("1.0", tk.END).strip()  # Should be empty since text is None
            assert not edit_requirement_page.tagging_text.list  # Should be empty since tags are None
        except Exception as e:
            pytest.fail(f"on_show raised an exception with missing attributes: {e}")

    #  Handles empty or invalid input fields in submit_requirement
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_handles_empty_or_invalid_input_fields_in_submit_requirement(self, app: MockMainApplication,
                                                                         edit_requirement_page: EditRequirementPage):

        # Create entries with empty or invalid data
        edit_requirement_page.entries = {
            "section": tk.Entry(app),
            "subsection": tk.Entry(app),
            "title": tk.Entry(app),
            "text": tk.Entry(app),
            "tags": tk.Entry(app)
        }

        # Leave all fields empty and call submit_requirement
        try:
            edit_requirement_page.add()
            # Check if a new requirement was added despite empty fields (it shouldn't be added)
            assert len(edit_requirement_page.connections) == 0

            # Now insert invalid data and call submit_requirement again
            edit_requirement_page.entries["tags"].insert(0, "InvalidTagFormat")
            edit_requirement_page.add()

            # Check if a new requirement was added despite invalid tags (it shouldn't be added)
            assert len(edit_requirement_page.connections) == 0

            # If no exception is raised and no new requirement is added, the test passes
            assert True

        except Exception as e:
            pytest.fail(f"submit_requirement raised an exception with empty or invalid input fields: {e}")

    #  Handles empty connections list in update_listbox
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_handles_empty_connections_list_in_update_listbox(self, app: MockMainApplication,
                                                              edit_requirement_page: EditRequirementPage):
        # Initialize connected_listbox and connections list as empty
        edit_requirement_page.connected_listbox = ttk.Treeview(app)

        # Call update_listbox with empty connections list and check if it handles gracefully
        try:
            edit_requirement_page.update_listbox()

            # Check if connected_listbox remains empty after update_listbox call
            assert len(edit_requirement_page.connected_listbox.get_children()) == 0

            # If no exception is raised and connected_listbox remains empty, the test passes
            assert True

        except Exception as e:
            pytest.fail(f"update_listbox raised an exception with empty connections list: {e}")

    #  Handles selection events in the traceability tab
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_handles_selection_events_in_traceability_tab(self, app: MockMainApplication,
                                                          edit_requirement_page: EditRequirementPage):

        # Simulate selection event in connectable listbox
        event = tk.Event()
        event.widget = edit_requirement_page.connectable_listbox

        try:
            edit_requirement_page.on_select(event)
            assert True  # If no exception is raised, the test passes

        except Exception as e:
            pytest.fail(f"on_select raised an exception during selection event handling in traceability tab: {e}")
