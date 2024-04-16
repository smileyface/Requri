import tkinter as tk

from UI.components.requirement_line_frame import RequirementFrame
from UI.components.scrollable_frame import ScrollableFrame
from structures import requirement_list
from UI.pages.paging_handle import show_page, PagesEnum, get_page




class RequirementsDisplayMain(ScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.requirement_frames = []

        self.update()

        self.bind("<Delete>", self.remove_selected)

    def add_requirement_frame(self, requirement):
        frame = RequirementFrame(self.scrollable_frame, requirement)
        frame.pack(fill=tk.X)
        self.requirement_frames.append(frame)

    def remove_requirement_frame(self, frame):
        frame.destroy()
        self.requirement_frames.remove(frame)

    def remove_selected(self, event):
        for frame in self.requirement_frames.copy():
            if frame.focus_get() is not None:
                index = self.requirement_frames.index(frame)
                requirement = requirement_list.get_requirement_from_index(index)
                requirement_list.remove(requirement)
                self.remove_requirement_frame(frame)
                break

    def edit_selected(self, event):
        for frame in self.requirement_frames:
            if frame.focus_get() is not None:
                index = self.requirement_frames.index(frame)
                requirement = requirement_list.get_requirement_from_index(index)
                if requirement:
                    get_page(PagesEnum.EDIT_REQUIREMENT).requirement = requirement
                    show_page(PagesEnum.EDIT_REQUIREMENT)
                    break

    def update(self):
        for frame in self.requirement_frames:
            frame.destroy()
        self.requirement_frames.clear()

        requirement_map = requirement_list.get_requirement_map()
        sorted_keys = sorted(requirement_map.keys(), key=lambda x: (x[0], x[1]))
        for requirement_section in sorted_keys:
            for requirement in requirement_map[requirement_section].values():
                self.add_requirement_frame(requirement)