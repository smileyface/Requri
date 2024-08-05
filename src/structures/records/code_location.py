import os
from dataclasses import field, dataclass


@dataclass
class Code_Location:
    DEFINITION: int = field(init=False, default=0)
    DECLARATION: int = field(init=False, default=1)

    location_type: int
    file: str
    begin: int
    end: int

    def __post_init__(self):
        self.file = os.path.abspath(self.file)
        if self.location_type not in [self.DEFINITION, self.DECLARATION]:
            raise ValueError("Invalid type parameter")
        if self.begin < 0 or self.end < 0 or self.begin > self.end:
            raise ValueError("Invalid begin or end values")