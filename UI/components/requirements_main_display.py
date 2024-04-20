import tkinter as tk

from UI.components.requirement_tile import RequirementTile
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

        # Configure rows and columns to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def add_requirement_frame(self, requirement):
        frame = RequirementTile(self.scrollable_frame, requirement)
        num_frames = len(self.requirement_frames)

        tile_width = 1
        if len(self.requirement_frames) > 0:
            tile_width = self.requirement_frames[0].winfo_width()
        frame_width = self.winfo_width()
        num_columns = max(1, frame_width // tile_width)


        row = num_frames // 3  # Distribute frames evenly across rows
        column = num_frames % 3  # Alternate between columns
        frame.grid(row=row, column=column, sticky="nsew")  # Use grid layout and expand in all directions
        self.requirement_frames.append(frame)

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

    def get_selected(self):
        selected = []
        for x in self.requirement_frames:
            if x.selected:
                selected.append(x)