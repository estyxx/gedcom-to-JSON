from pathlib import Path

import pytest

from gedcom.exceptions import FileAlreadyExistsError
from gedcom.family import Family
from gedcom.file import File
from gedcom.individual import Individual


def test_get_individuals():
    file = File(
        elements=[
            Individual(name="Ester"),
            Individual(name="Toby"),
        ]
    )

    assert file.individuals == [
        Individual(name="Ester"),
        Individual(name="Toby"),
    ]


def test_get_families():
    file = File(
        elements=[
            Family(wife="Mortisia", husband="Gomez"),
            Family(wife="Belle", husband="The Beast"),
        ]
    )

    assert file.families == [
        Family(wife="Mortisia", husband="Gomez"),
        Family(wife="Belle", husband="The Beast"),
    ]


@pytest.fixture
def file_already_exists():
    path = Path("pytest.json")

    with path.open("w") as f:
        f.write("something")

    yield str(path)

    if path.exists():
        path.unlink()


def test_raise_error_if_file_alrady_exists(file_already_exists):
    with pytest.raises(
        FileAlreadyExistsError, match=f"File '{file_already_exists}' already exists"
    ):
        file = File(filename=file_already_exists)
        file.save()


@pytest.fixture
def file_example():
    path = Path("pytest.json")

    yield str(path)

    if path.exists():
        path.unlink()


def test_save_file(file_example):

    file = File(filename=file_example)

    file.save()

    with Path(file_example).open("r") as f:
        assert f.read() == "lorem\nipsum\nsum\n"
