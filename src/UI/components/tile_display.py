from UI.tiles.code_tile import CodeTile
from UI.tiles.requirement_tile import RequirementTile
from UI.components.scrollable_frame import ScrollableFrame
from structures.lists import requirement_list
from structures.records.code import Code
from structures.records.requirement import Requirement
from lexical.search import interpret


class TileView(ScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.tiles = []
        self.selected_frame = None  # Track the currently selected frame
        self._last_width = 0
        self.query = "all"

        self.update()

        self.bind("<Delete>", self.remove_selected)
        self.bind("<Configure>", self.on_configure)

        # Configure rows and columns to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_tile_from_record(self, record):
        if isinstance(record, Requirement):
            frame = RequirementTile(self.scrollable_frame, record)
        elif isinstance(record, Code):
            frame = CodeTile(self.scrollable_frame, record)
        return frame

    def add_tile(self, data):
        frame = self.create_tile_from_record(data)
        self.tiles.append(frame)

    def place_tiles(self):
        # Remove existing tiles without destroying other children
        for tile in self.tiles:
            tile.update()
            tile.grid_forget()  # Remove the tile from the grid layout

        # Calculate the number of columns based on frame width
        frame_width = self.winfo_width()
        num_columns = max(1, (frame_width // 256) - 1)

        # Place tiles using grid layout
        for i, tile in enumerate(self.tiles):
            row = i // num_columns
            column = i % num_columns
            tile.grid(row=row, column=column, sticky="nsew")

        # Update the scrollable region
        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

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

    def update_content(self, index, record):
        self.tiles[index].data = record

    def update(self):
        # Get the requirement map and calculate the number of columns
        record_map = interpret(self.query)

        num_frames = len(record_map)

        for i, record in enumerate(record_map):
            if i < len(self.tiles):
                # If the tile exists, update its content
                self.update_content(i, record)
            else:
                # If the tile doesn't exist, create a new one
                self.add_tile(record)

        # Remove any extra tiles if the number of records decreased
        if len(self.tiles) > num_frames:
            for frame in self.tiles[num_frames:]:
                self.remove_tile(frame)
        self.place_tiles()
        # Reset selected frame after updating tiles
        self.selected_frame = None

    def get_selected(self):
        selected = []
        for x in self.tiles:
            if x.selected:
                selected.append(x)

    def on_configure(self, event):
        self.update()
