import logging
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch

import pytest

from UI.pages.paging_handle import PagingHandle, PagesEnum
from UI.pages import requirements
from UI.pages.viewpage import ViewPage
from structures.lists import requirement_list
from structures.records import Code, Requirement
from structures.records.record import Record
from testing.utils.decorators import main_app_test
from testing.fixtures.app_fixtures import app, page
from testing.tests.ui.page.mock_main_app import MockMainApplication

# Set up logging to output to the console
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class TestAddRequirementPage:

    @pytest.fixture(autouse=True)
    def teardown(self):
        yield
        Record.clear_records()
        requirement_list.clear_list()
        PagingHandle.clear_paging_handler()

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_all_components_initialization_and_locations(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify that all UI components are properly initialized and located.
        """

        # Access the notebook widget
        notebook = page.nametowidget('add_requirement_body')
        assert isinstance(notebook, ttk.Notebook)

        # Verify the notebook has two tabs
        assert notebook.index("end") == 2

        # Verify the text of the tabs
        assert notebook.tab(0, "text") == "Add Requirement"
        assert notebook.tab(1, "text") == "Traceability"

        # Access the tabs by name
        requirement_tab = notebook.nametowidget('add_requirements_req_tab')
        traceability_tab = notebook.nametowidget('add_requirements_trace_tab')

        # Verify the components in the requirement tab
        assert page.title_label.winfo_ismapped()
        assert page.title_entry.winfo_ismapped()
        assert page.section_label.winfo_ismapped()
        assert page.section.winfo_ismapped()
        assert page.subsection_label.winfo_ismapped()
        assert page.subsection.winfo_ismapped()
        assert page.tagging_label.winfo_ismapped()
        assert page.tagging_text.winfo_ismapped()
        assert page.requirement_label.winfo_ismapped()
        assert page.requirement_text.winfo_ismapped()

        # Verify the components in the traceability tab
        notebook.select(traceability_tab)
        app.update_idletasks()  # Ensure the GUI updates the tab selection

        # Verify the components in the traceability tab
        assert page.connectable_listbox.winfo_ismapped()
        assert page.connected_listbox.winfo_ismapped()

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_switching_tabs(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify that switching between tabs works correctly.
        """
        # Access the notebook widget
        notebook = page.nametowidget('add_requirement_body')
        assert isinstance(notebook, ttk.Notebook)

        # Access the tabs by name
        requirement_tab = notebook.nametowidget('add_requirements_req_tab')
        traceability_tab = notebook.nametowidget('add_requirements_trace_tab')

        # Switch to the Traceability tab
        notebook.select(traceability_tab)
        app.update_idletasks()  # Ensure the GUI updates the tab selection

        # Verify the Traceability tab is selected
        assert notebook.select() == traceability_tab._w

        # Verify the components in the Traceability tab are mapped
        assert page.connectable_listbox.winfo_ismapped()
        assert page.connected_listbox.winfo_ismapped()

        # Switch back to the Add Requirement tab
        notebook.select(requirement_tab)
        app.update_idletasks()  # Ensure the GUI updates the tab selection

        # Verify the Add Requirement tab is selected
        assert notebook.select() == requirement_tab._w

        # Verify the components in the Add Requirement tab are mapped
        assert page.title_label.winfo_ismapped()
        assert page.title_entry.winfo_ismapped()
        assert page.section_label.winfo_ismapped()
        assert page.section.winfo_ismapped()
        assert page.subsection_label.winfo_ismapped()
        assert page.subsection.winfo_ismapped()
        assert page.tagging_label.winfo_ismapped()
        assert page.tagging_text.winfo_ismapped()
        assert page.requirement_label.winfo_ismapped()
        assert page.requirement_text.winfo_ismapped()

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_adds_code_items_to_treeview_under_implementations(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Successfully adds Code items to the treeview under 'Implementations'.
        """
        treeview = ttk.Treeview(app)
        connected_items = [Code("file1", "public", "Class1", "method1", ["arg1", "arg2"], 1, 21, True)]
        page = requirements.AddRequirementPage(app)
        page._add_lists_to_treeview(connected_items, treeview)
        assert treeview.get_children() == ('I001',)
        assert treeview.item('I001', 'text') == 'Implementations'
        assert treeview.get_children('I001') == ('Code-0',)

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_adds_requirement_items_to_treeview_under_related_requirements(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Successfully adds Requirement items to the treeview under 'Related Requirements'.
        """
        treeview = ttk.Treeview(app)
        connected_items = [Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"])]
        page._add_lists_to_treeview(connected_items, treeview)
        assert treeview.get_children() == ('I001',)
        assert treeview.item('I001', 'text') == 'Related Requirements'
        assert treeview.get_children('I001') == ('Req-section1-subsection1-0',)

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_handles_mixed_lists_of_code_and_requirement_items(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Handles mixed lists of Code and Requirement items correctly.
        """
        treeview = ttk.Treeview(app)
        connected_items = [
            Code("file1", "public", "Class1", "method1", ["arg1", "arg2"], 1, 21, True),
            Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"])
        ]
        page._add_lists_to_treeview(connected_items, treeview)
        assert len(treeview.get_children()) == 2
        assert treeview.item(treeview.get_children()[0], 'text') == 'Related Requirements'
        assert treeview.item(treeview.get_children()[1], 'text') == 'Implementations'

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_maintains_order_of_items_as_per_input_list(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Maintains the order of items as per the input list.
        """
        treeview = ttk.Treeview(app)
        connected_items = [
            Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"]),
            Code("file2", "private", "Class2", "method2", ["arg3", "arg4"], 1, 21, False)
        ]
        page._add_lists_to_treeview(connected_items, treeview)
        children = treeview.get_children()
        assert len(children) == 2
        assert treeview.item(children[0], 'text') == 'Related Requirements'
        assert treeview.item(children[1], 'text') == 'Implementations'

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_handles_empty_list_without_errors(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Handles empty lists without errors.
        """
        treeview = ttk.Treeview(app)
        connected_items = []
        page._add_lists_to_treeview(connected_items, treeview)
        assert len(treeview.get_children()) == 0

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_manages_lists_with_only_code_items(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Manages lists with only Code items.
        """
        treeview = ttk.Treeview(app)
        connected_items = [
            Code("file1", "public", "Class1", "method1", ["arg1", "arg2"], 1, 21, True),
        ]
        page._add_lists_to_treeview(connected_items, treeview)
        assert len(treeview.get_children()) == 1
        assert treeview.item(treeview.get_children()[0], 'text') == 'Implementations'

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_handles_missing_or_none_unique_ids(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Handles missing or None unique IDs gracefully.
        """
        treeview = ttk.Treeview(app)
        connected_items = [
            Code("file1", "public", "Class1", "method1", ["arg1", "arg2"], 1, 21, True),
            Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"], new_unique_id=None)
        ]
        page._add_lists_to_treeview(connected_items, treeview)
        assert len(treeview.get_children()) == 2

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_logs_errors_when_insertion_fails(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Logs errors when insertion into the treeview fails.
        """
        treeview = ttk.Treeview(app)

        class FaultyCode(Code):
            @property
            def unique_id(self):
                raise ValueError("Faulty ID")

        connected_items = [FaultyCode("file3", "protected", "Class3", "method3", ["arg5"], 1, 21, True)]

        with pytest.raises(ValueError):
            page._add_lists_to_treeview(connected_items, treeview)

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_handles_faulty_code_items_that_raise_exceptions(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Handles faulty Code items that raise exceptions gracefully.
        """
        treeview = ttk.Treeview(app)

        class FaultyCode(Code):
            @property
            def unique_id(self):
                raise ValueError("Faulty ID")

        connected_items = [FaultyCode("file3", "protected", "Class3", "method3", ["arg5"], 1, 21, True)]

        with pytest.raises(ValueError):
            page._add_lists_to_treeview(connected_items, treeview)

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_handles_drag_and_drop_events_with_invalid_data(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Handles drag and drop events with invalid data gracefully.
        """

        class MockEvent:
            def __init__(self, widget, x_root, y_root):
                self.widget = widget
                self.x_root = x_root
                self.y_root = y_root

            @property
            def x(self):
                return self.x_root

            @property
            def y(self):
                return self.y_root

        mock_widget = tk.Label(app, text='mock_widget')
        mock_widget._drag_data = None  # Invalid data

        event = MockEvent(mock_widget, 100, 100)

        page.on_drop(event)  # Should handle gracefully without errors

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_manages_lists_with_only_requirement_items(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Manages lists with only Requirement items.
        """
        treeview = ttk.Treeview(app)
        connected_items = [
            Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"]),
            Requirement("section2", "subsection2", "Title2", "Text2", ["tag2"])
        ]
        page._add_lists_to_treeview(connected_items, treeview)
        assert len(treeview.get_children()) == 2
        assert treeview.item(treeview.get_children()[0], 'text') == 'Related Requirements'

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_handles_large_lists_efficiently(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Handles large lists efficiently.
        """
        treeview = ttk.Treeview(app)

        connected_items = [
            Code(f"file{i}", f"access{i}", f"Class{i}", f"method{i}", [f"arg{i}"], i, i + 1, True) for i
            in range(1000)]

        import time
        start_time = time.time()

        page._add_lists_to_treeview(connected_items, treeview)

        end_time = time.time()

        assert (end_time - start_time) < 5  # Ensure it runs within 5 seconds for 1000 items

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_ui_component_initialization(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify that all UI components are properly initialized and visible.
        """
        assert page.title_label.cget("text") == "Title:"
        assert page.section_label.cget("text") == "Section:"
        assert page.subsection_label.cget("text") == "Subsection:"
        assert page.tagging_label.cget("text") == "Tags:"
        assert page.requirement_label.cget("text") == "Requirement:"

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_requirement_addition(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify that a requirement is correctly added to the requirement list.
        """
        page.title_entry.insert(0, "Test Requirement")
        page.section.variable.set("Test Section")
        page.subsection.variable.set("Test Subsection")
        page.requirement_text.insert("1.0", "This is a test requirement.")
        page.tagging_text.list = ["tag1", "tag2"]

        page.add()

        added_req = requirement_list.get_requirement_list()[-1]
        assert added_req.title == "Test Requirement"
        assert added_req.section == "Test Section"
        assert added_req.sub == "Test Subsection"
        assert added_req.text == "This is a test requirement."
        assert added_req.tags == ["tag1", "tag2"]

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_cancel_operation(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify that the cancel operation navigates back to the previous page.
        """
        with patch('UI.pages.paging_handle.PagingHandle.page_return', autospec=True) as mock_page_return:
            page.cancel()
            mock_page_return.assert_called_once()

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_section_and_subsection_updates(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify that selecting a section updates the subsection combobox correctly.
        """
        page.section.variable.set("Section 1")
        requirement_list.append(Requirement("Section 1", "Subsection 1.1", "", "", []))
        requirement_list.append(Requirement("Section 1", "Subsection 1.2", "", "", []))
        page.update_combobox_b()
        assert "Subsection 1.1" in page.subsection.cget("values")
        assert "Subsection 1.2" in page.subsection.cget("values")

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_tag_autocompletion(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify that the autocomplete functionality for tags works correctly.
        """
        page.tagging_text.entry.insert(0, "#tag")
        event = tk.Event()
        event.keysym = 'numbersign'
        page.tagging_text.check_trigger(event)
        assert page.tagging_text.option_list.size() > 0

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_drag_and_drop_functionality(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify the drag and drop functionality with valid and invalid data.
        """
        page.connections = []  # Ensure connections is initialized
        # Simulate a valid drag and drop operation
        page.connectable_listbox.insert("", "end", iid="item1", text="Item 1")
        page.connectable_listbox.selection_set("item1")

        valid_event = tk.Event()
        valid_event.widget = page.connectable_listbox
        valid_event.x_root = page.connectable_listbox.winfo_rootx() + 10
        valid_event.y_root = page.connectable_listbox.winfo_rooty() + 10

        page.on_drag(valid_event)

        valid_event.widget = page.connected_listbox
        valid_event.x_root = page.connected_listbox.winfo_rootx() + 10
        valid_event.y_root = page.connected_listbox.winfo_rooty() + 10

        page.on_drop(valid_event)
        assert len(page.connections) > 0
        # Simulate an invalid drag and drop operation
        invalid_event = tk.Event()
        invalid_event.widget = page.connectable_listbox
        invalid_event.x_root = page.connectable_listbox.winfo_rootx() + 10
        invalid_event.y_root = page.connectable_listbox.winfo_rooty() + 10

        page.on_drag(invalid_event)

        invalid_event.widget = page.connected_listbox
        invalid_event.x_root = page.connected_listbox.winfo_rootx() + 10
        invalid_event.y_root = page.connected_listbox.winfo_rooty() + 10

        page.on_drop(invalid_event)
        assert len(page.connections) > 0  # Should handle gracefully without errors

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_ui_layout_and_resizing(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Ensure the layout adjusts correctly when the window is resized.
        """
        app.geometry("800x600")
        app.update_idletasks()
        initial_size = page.requirement_text.winfo_height()
        app.geometry("600x400")
        app.update_idletasks()
        resized_size = page.requirement_text.winfo_height()
        assert resized_size != initial_size

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_add_empty_requirement(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify that adding an empty requirement shows an error or does not add.
        """
        page.add()
        assert len(requirement_list.get_requirement_list()) == 0  # Assuming the list should remain empty

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_add_duplicate_requirement(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify that adding duplicate requirements is handled correctly.
        """
        page.title_entry.insert(0, "Test Requirement")
        page.section.variable.set("Test Section")
        page.subsection.variable.set("Test Subsection")
        page.requirement_text.insert("1.0", "This is a test requirement.")
        page.tagging_text.list = ["tag1", "tag2"]

        page.add()
        page.add()  # Attempt to add the same requirement again

        assert len(requirement_list.get_requirement_list()) == 1  # Should not add duplicate

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_add_requirement_with_max_length_values(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify adding a requirement with maximum length values for fields.
        """
        long_text = "a" * 1000
        page.title_entry.insert(0, long_text)
        page.section.variable.set(long_text)
        page.subsection.variable.set(long_text)
        page.requirement_text.insert("1.0", long_text)
        page.tagging_text.list = [long_text]

        page.add()

        added_req = requirement_list.get_requirement_list()[-1]
        assert added_req.title == long_text
        assert added_req.section == long_text
        assert added_req.sub == long_text
        assert added_req.text == long_text
        assert added_req.tags == [long_text]

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_add_requirement_with_special_characters(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify adding a requirement with special characters in fields.
        """
        special_text = "!@#$%^&*()_+"
        page.title_entry.insert(0, special_text)
        page.section.variable.set(special_text)
        page.subsection.variable.set(special_text)
        page.requirement_text.insert("1.0", special_text)
        page.tagging_text.list = [special_text]

        page.add()

        added_req = requirement_list.get_requirement_list()[-1]
        assert added_req.title == special_text
        assert added_req.section == special_text
        assert added_req.sub == special_text
        assert added_req.text == special_text
        assert added_req.tags == [special_text]

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_error_handling_on_invalid_data(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify error handling when invalid data is provided.
        """
        # Simulate invalid data scenario
        with patch('structures.lists.requirement_list.append', side_effect=Exception("Test Error")):
            page.add()
            # Verify that the error was logged or handled gracefully
            # Adjust this assertion based on your error handling implementation
            assert len(requirement_list.get_requirement_list()) == 0

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_state_persistence_on_navigation(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify state persistence when navigating between pages.
        """
        page.title_entry.insert(0, "Persistent Requirement")
        page.section.variable.set("Persistent Section")
        page.subsection.variable.set("Persistent Subsection")
        page.requirement_text.insert("1.0", "Persistent text")
        page.tagging_text.list = ["persistent_tag"]

        # Simulate navigation
        PagingHandle.show_page(PagesEnum.RECORD_VIEW)
        PagingHandle.show_page(PagesEnum.ADD_REQUIREMENT)

        # Verify state persistence
        assert page.title_entry.get() == "Persistent Requirement"
        assert page.section.variable.get() == "Persistent Section"
        assert page.subsection.variable.get() == "Persistent Subsection"
        assert page.requirement_text.get("1.0", "end-1c") == "Persistent text"
        assert page.tagging_text.list == ["persistent_tag"]

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_component_visibility_based_on_input(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify the visibility of components based on certain inputs.
        """
        page.section.variable.set("Some Section")
        requirement_list.append(Requirement("Some Section", "Subsection 1", "", "", []))
        page.update_combobox_b()

        # Verify that subsection is updated and visible
        # Subsection defaults to "", then selection happens by user.
        assert page.subsection.variable.get() == ""
        assert page.subsection.winfo_ismapped()

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_event_triggered_actions(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify that correct actions are triggered on various UI events.
        """
        # Simulate button click event
        page.add_button.invoke()
        assert len(requirement_list.get_requirement_list()) == 0  # Assuming no valid data to add

        page.cancel_button.invoke()
        # Assuming PagingHandle.page_return() should be called
        with patch('UI.pages.paging_handle.PagingHandle.page_return', autospec=True) as mock_page_return:
            page.cancel()
            mock_page_return.assert_called_once()

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_combobox_options_update(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify that the ComboboxWithAdd options are correctly updated when the update_combobox_b method is triggered by a section change.
        """
        section_options = ["Section 1", "Section 2"]
        page.section.set_options(section_options)
        page.section.variable.set("Section 1")

        requirement_list.append(Requirement("Section 1", "Subsection 1.1", "", "", []))
        requirement_list.append(Requirement("Section 1", "Subsection 1.2", "", "", []))
        page.update_combobox_b()

        assert "Subsection 1.1" in page.subsection.cget("values")
        assert "Subsection 1.2" in page.subsection.cget("values")

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_error_handling_on_ui_components(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Simulate errors in UI components and verify that they are handled gracefully.
        """
        # Simulate error in ComboboxWithAdd
        with patch.object(page.section, 'set_options', side_effect=Exception("Test Error")):
            page.section.set_options(["Option 1", "Option 2"])
            assert page.section.cget("values") == ('',)  # Default value

        # Simulate error in AutoCompleteEntry
        with patch.object(page.tagging_text, 'configure', side_effect=Exception("Test Error")):
            page.tagging_text.configure(choices=["Tag 1", "Tag 2"])
            assert page.tagging_text.cget("values") == ''  # Default value

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_update_combobox_b_with_invalid_section(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify the behavior when an invalid section is selected.
        """
        page.section.variable.set("Invalid Section")
        page.update_combobox_b()
        assert page.subsection.cget("values") == ('',)

    @main_app_test(PagesEnum.ADD_REQUIREMENT)
    def test_ui_state_reset_on_reload(self, app: MockMainApplication, page: ViewPage):
        """
        Test: Verify that the UI components are reset correctly when the page is reloaded.
        """
        page.title_entry.insert(0, "Persistent Requirement")
        page.section.variable.set("Persistent Section")
        page.subsection.variable.set("Persistent Subsection")
        page.requirement_text.insert("1.0", "Persistent text")
        page.tagging_text.list = ["persistent_tag"]

        # Simulate page reload
        page.create_body()
        app.update()  # Ensure all widgets are updated

        # Verify state reset
        assert page.title_entry.get() == ""
        assert page.section.variable.get() == ""
        assert page.subsection.variable.get() == ""
        assert page.requirement_text.get("1.0", "end-1c") == ""
        assert page.tagging_text.list == []
