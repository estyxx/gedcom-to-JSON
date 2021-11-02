from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, List, Union

from gedcom.exceptions import FileAlreadyExistsError
from gedcom.family import Family
from gedcom.individual import Individual


@dataclass
class File:
    elements: List[Union[Individual, Family]] = field(default_factory=list)
    filename: str = "output.json"

    @property
    def individuals(self) -> List[Individual]:
        return list(e for e in self.elements if isinstance(e, Individual))

    @property
    def families(self) -> List[Family]:
        return list(e for e in self.elements if isinstance(e, Family))

    def lines(self) -> Iterator[str]:
        _lines = ["lorem", "ipsum", "sum"]
        for l in _lines:
            yield l

    def save(self):
        if Path(self.filename).exists():
            raise FileAlreadyExistsError(self.filename)

        with Path(self.filename).open("wb") as f:

            for line in self.lines():
                f.write(line.encode("utf8"))
                f.write("\n".encode("utf8"))
