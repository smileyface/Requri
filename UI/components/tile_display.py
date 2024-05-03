from UI.tiles.code_tile import CodeTile
from UI.tiles.requirement_tile import RequirementTile
from UI.components.scrollable_frame import ScrollableFrame
from structures import requirement_list
from structures.code import Code
from structures.code_list import code_list
from structures.requirement import Requirement


class TileView(ScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.tiles = []
        self.selected_frame = None  # Track the currently selected frame
        self._last_width = 0

        self.update()

        self.bind("<Delete>", self.remove_selected)
        self.bind("<Configure>", self.on_configure)

        # Configure rows and columns to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def add_tile(self, data):
        if isinstance(data, Requirement):
            frame = RequirementTile(self.scrollable_frame, data)
        elif isinstance(data, Code):
            frame = CodeTile(self.scrollable_frame, data)
        num_frames = len(self.tiles)

        tile_width = 1
        if len(self.tiles) > 0:
            tile_width = self.tiles[0].winfo_width()
        frame_width = self.winfo_width()
        num_columns = max(1, (frame_width // 256) - 1)

        row = num_frames // num_columns  # Distribute frames evenly across rows
        column = num_frames % num_columns  # Alternate between columns
        frame.grid(row=row, column=column, sticky="nsew")  # Use grid layout and expand in all directions
        self.tiles.append(frame)

    def remove_tile(self, frame):
        frame.destroy()
        self.tiles.remove(frame)

    def remove_selected(self, event):
        if self.selected_frame:
            index = self.tiles.index(self.selected_frame)
            requirement = requirement_list.get_requirement_from_index(index)
            requirement_list.remove(requirement)
            self.remove_tile(self.selected_frame)
            self.selected_frame = None  # Reset selected frame after removal

    def update(self):
        # Check if the size of the widget has changed
        current_width = self.winfo_width()

        # Clear existing tiles
        for frame in self.tiles:
            frame.destroy()
        self.tiles.clear()

        # Get the requirement map and calculate the number of columns
        requirement_map = requirement_list.get_requirement_map()
        sorted_keys = sorted(requirement_map.keys(), key=lambda x: (x[0], x[1]))

        # Add tiles based on the requirement map
        for requirement_section in sorted_keys:
            for requirement in requirement_map[requirement_section].values():
                self.add_tile(requirement)

        for code_section in code_list.keys():
            self.add_tile(code_list[code_section])

    def get_selected(self):
        selected = []
        for x in self.tiles:
            if x.selected:
                selected.append(x)

    def on_configure(self, event):
        self.update()
