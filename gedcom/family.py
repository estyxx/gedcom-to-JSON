from dataclasses import dataclass
from typing import Optional


@dataclass
class Family:
    wife: Optional[str] = None
    husband: Optional[str] = None
