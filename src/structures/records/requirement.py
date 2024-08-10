import logging
from dataclasses import dataclass, InitVar, field
from typing import List, Dict, Optional

from src.structures.records import Code
from src.structures.records.record import Record
from src.structures.requirement_id import RequirementId


@dataclass
class Requirement(Record):
    section: str
    sub: str
    title: str
    text: str
    tags: List[str]
    new_unique_id: InitVar[Optional[int]] = None
    _unique_id: RequirementId = field(init=False)

    def __post_init__(self, new_unique_id: Optional[int]):
        if not isinstance(self.tags, list):
            raise TypeError("`tags` must be a list.")
        super().__init__(self.tags)
        self._unique_id = RequirementId(self.section, self.sub, new_unique_id)
        self.text = self.text.strip() if self.text else ''

    def __del__(self):
        logging.info(f"Deleting Requirement: {self.unique_id}")
        super().__del__()
        del self._unique_id
        pass


    @property
    def unique_id(self) -> RequirementId:
        """Property that returns the unique identifier of the requirement."""
        return self._unique_id

    def __repr__(self) -> str:
        """Return a string representation of the Requirement object."""
        connection_str = ""
        if Code in self.connections and self.connections[Code]:
            connection_str = " (Connected to "
            for x in self.connections[Code]:
                connection_str += f"{x}"
            connection_str += ")"
        return f"{self.unique_id}: {self.title}{connection_str}"

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
