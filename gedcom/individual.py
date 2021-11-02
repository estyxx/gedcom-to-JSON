from dataclasses import dataclass
from typing import Optional


@dataclass
class Individual:
    name: Optional[str]

    def __str__(self):
        return self.name
