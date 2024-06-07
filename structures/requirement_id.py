import logging
from dataclasses import dataclass, InitVar, field
from typing import Dict, Optional

@dataclass
class RequirementId:
    section: str
    sub: str
    new_unique_id: InitVar[Optional[int]] = None
    _unique_id: Optional[int] = field(init=False, default=None)
    id_range_max: int = 99999

    id_map = dict()
    def __post_init__(self, new_unique_id: Optional[int]):
        if new_unique_id is not None:
            self.unique_id = new_unique_id

    def __str__(self) -> str:
        """Return a string representation of the RequirementId object."""
        parts = [self.section + '-' if self.section else '', self.sub + '-' if self.sub else '']
        return ''.join(parts) + str(self.unique_id)

    def __del__(self):
        location = (self.section, self.sub)
        if self._unique_id is not None and location in self.id_map:
            self.id_map[location].remove(self._unique_id)
        self._unique_id = None

    @property
    def unique_id(self) -> int:
        if self._unique_id is None:
            self._unique_id = self._create_unique_id()
            logging.info(f"Unique ID created and assigned: {self._unique_id} for section {self.section} and sub {self.sub}")
        return self._unique_id

    @unique_id.setter
    def unique_id(self, id: int):
        location = (self.section, self.sub)
        if location not in self.id_map:
            self.id_map[location] = []
        if id < 0 or id > self.id_range_max:
            raise ValueError("ID out of range")
        if id in self.id_map[location]:
            raise ValueError("Non Unique ID")

        if self._unique_id in self.id_map[location]:
            self.id_map[location].remove(self._unique_id)
        self.id_map[location].append(id)
        self._unique_id = id


    def _create_unique_id(self) -> int:
        location = (self.section, self.sub)
        if location not in self.id_map:
            self.id_map[location] = [0]
            return 0
        else:
            for x in range(self.id_range_max):
                if x not in self.id_map[location]:
                    self.id_map[location].append(x)
                    return x



    def to_json(self) -> Dict[str, str]:
        return {"section": self.section, "sub": self.sub, "id": self.unique_id}
