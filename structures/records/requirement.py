from typing import List, Dict

from structures.records import Code
from structures.records.record import Record
from structures.requirement_id import RequirementId


class Requirement(Record):
    """Represents a requirement with a unique identifier, title, text, and tags."""
    
    def __init__(self, section: str, sub: str, title: str, text: str, tags: List[str], unique_id: int = None):
        """
        Initializes a new requirement with the given section, subsection, title, text, tags, and optional unique ID.
        
        Args:
        - section: The section of the requirement.
        - sub: The subsection of the requirement.
        - title: The title of the requirement.
        - text: The text of the requirement.
        - tags: List of tags associated with the requirement.
        - unique_id: Optional unique ID for the requirement.
        """
        if not isinstance(tags, list):
            raise TypeError("`tags` must be a list.")
        super().__init__(tags)
        self._unique_id = RequirementId(section, sub, unique_id)
        self.text = text.strip() if text else ''
        self.title = title

    def connect(self, connection):
        """
        Connects the requirement to another requirement or code instance.
        
        Args:
        - connection: The requirement or code instance to connect to.
        """
        if isinstance(connection, Requirement):
            self.connections["Supporting Requirement"] = connection
        elif isinstance(connection, Code):
            self.connections["Implementation"] = connection
        else:
            super().connect(connection)

    @property
    def unique_id(self) -> RequirementId:
        """Property that returns the unique identifier of the requirement."""
        return self._unique_id

    def __repr__(self) -> str:
        """Return a string representation of the Requirement object."""
        return f"{self.unique_id}: {self.title}"

    def to_json(self) -> Dict:
        """Converts the requirement to a JSON representation."""
        return {"id": self._unique_id.to_json(), "title": self.title, "text": self.text, "tags": self.tags}

    def to_markdown(self) -> str:
        """
        Converts the requirement to a markdown representation.

        Returns:
        - A string containing the markdown representation of the requirement.
        """
        tags_str = ', '.join(self.tags)
        return f"## {self.title}\n\n**ID:** {self.unique_id}\n\n**Text:**\n\n{self.text}\n\n**Tags:** {tags_str}\n"
