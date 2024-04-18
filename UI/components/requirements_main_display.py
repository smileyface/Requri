import tkinter as tk

from UI.components.requirement_line_frame import RequirementFrame
from UI.components.scrollable_frame import ScrollableFrame
from structures import requirement_list
from UI.pages.paging_handle import show_page, PagesEnum, get_page


class RequirementsDisplayMain(ScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.requirement_frames = []
        self.selected_frame = None  # Track the currently selected frame

        self.update()

        self.bind("<Delete>", self.remove_selected)

    def add_requirement_frame(self, requirement):
        frame = RequirementFrame(self.scrollable_frame, requirement)
        frame.pack(side=tk.TOP, fill=tk.X)
        self.requirement_frames.append(frame)
        frame.bind("<Button-1>", lambda event, frame=frame: self.toggle_selection(event, frame))

    def remove_requirement_frame(self, frame):
        frame.destroy()
        self.requirement_frames.remove(frame)

    def remove_selected(self, event):
        if self.selected_frame:
            index = self.requirement_frames.index(self.selected_frame)
            requirement = requirement_list.get_requirement_from_index(index)
            requirement_list.remove(requirement)
            self.remove_requirement_frame(self.selected_frame)
            self.selected_frame = None  # Reset selected frame after removal

    def edit_selected(self, event):
        if self.selected_frame:
            index = self.requirement_frames.index(self.selected_frame)
            requirement = requirement_list.get_requirement_from_index(index)
            if requirement:
                get_page(PagesEnum.EDIT_REQUIREMENT).requirement = requirement
                show_page(PagesEnum.EDIT_REQUIREMENT)

    def update(self):
        for frame in self.requirement_frames:
            frame.destroy()
        self.requirement_frames.clear()

        requirement_map = requirement_list.get_requirement_map()
        sorted_keys = sorted(requirement_map.keys(), key=lambda x: (x[0], x[1]))
        for requirement_section in sorted_keys:
            for requirement in requirement_map[requirement_section].values():
                self.add_requirement_frame(requirement)

    def toggle_selection(self, event, frame):
        print("Toggle selection called")
        # Deselect previously selected frame (if any)
        if self.selected_frame and self.selected_frame in self.requirement_frames:
            print("Deselecting previous frame")
            self.selected_frame.config(borderwidth=1, relief=tk.SOLID)
        # Toggle selection for the clicked frame
        if frame == self.selected_frame:
            print("Frame is already selected, deselecting")
            self.selected_frame = None
        else:
            print("Selecting new frame")
            self.selected_frame = frame
            frame.config(borderwidth=2, relief=tk.SOLID, highlightbackground="blue")