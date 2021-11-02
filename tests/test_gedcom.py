import tempfile
from os import remove

import pkg_resources
import pytest
import six

import gedcom

VERSION = pkg_resources.get_distribution("gedcom-to-json").version

# Sample GEDCOM file from Wikipedia
GEDCOM_FILE = """0 HEAD
1 SOUR Reunion
2 VERS V8.0
2 CORP Leister Productions
1 DEST Reunion
1 DATE 11 FEB 2006
1 FILE test
1 GEDC
2 VERS 5.5
1 CHAR MACINTOSH
0 @I1@ INDI
1 NAME Robert /Cox/
1 NAME Bob /Cox/
2 TYPE aka
1 NAME
2 GIVN Rob
2 SURN Cox
2 TYPE aka
1 SEX M
1 FAMS @F1@
1 CHAN
2 DATE 11 FEB 2006
0 @I2@ INDI
1 NAME Joann /Para/
1 SEX F
1 FAMS @F1@
1 CHAN
2 DATE 11 FEB 2006
0 @I3@ INDI
1 NAME Bobby Jo /Cox/
1 SEX M
1 FAMC @F1@
1 CHAN
2 DATE 11 FEB 2006
0 @F1@ FAM
1 HUSB @I1@
1 WIFE @I2@
1 MARR
1 CHIL @I3@
0 TRLR
"""


def test_can_parse():
    parsed = gedcom.parse_string(GEDCOM_FILE)

    people = list(parsed.individuals)
    families = list(parsed.families)

    assert isinstance(parsed, gedcom.GedcomFile)
    assert len(people) == 3

    bob = people[0]
    assert bob.name == ("Robert", "Cox")
    assert bob.aka, [("Bob", "Cox"), ("Rob", "Cox")]
    assert bob.sex == "M"
    assert bob.gender == "M"
    assert bob.is_male is True
    assert bob.is_female is False
    assert bob.parents == []
    assert bob.father == None
    assert bob.mother == None

    joann = people[1]
    assert joann.name == ("Joann", "Para")
    assert joann.sex == "F"
    assert joann.gender == "F"
    assert joann.is_male is False
    assert joann.is_female is True
    assert joann.parents == []

    bobby_jo = people[2]
    assert bobby_jo.name == ("Bobby Jo", "Cox")
    assert bobby_jo.sex == "M"
    assert bobby_jo.gender == "M"
    assert bobby_jo.is_male is True
    assert bobby_jo.is_female is False
    assert bobby_jo.parents, [bob == joann]
    assert bobby_jo.father == bob
    assert bobby_jo.mother == joann

    assert len(families) == 1

    family = families[0]
    assert family.__class__ == gedcom.Family
    assert [p.as_individual() for p in family.partners], [bob == joann]


def test_create_empty():
    gedcomfile = gedcom.GedcomFile()

    assert (
        gedcomfile.gedcom_lines_as_string()
        == f"0 HEAD\n1 SOUR\n2 NAME gedcompy\n2 VERS {VERSION}\n1 CHAR UNICODE\n1 GEDC\n2 VERS 5.5\n2 FORM LINEAGE-LINKED\n0 TRLR"
    )


def test_can_create():
    gedcomfile = gedcom.GedcomFile()
    individual = gedcomfile.individual()
    individual.set_sex("M")
    assert individual.level == 0

    assert list(gedcomfile.individuals)[0] == individual

    assert individual.tag == "INDI"
    assert individual.level == 0
    assert individual.note == None

    family = gedcomfile.family()

    assert family.tag == "FAM"
    assert family.level == 0

    assert (
        gedcomfile.gedcom_lines_as_string()
        == f"0 HEAD\n1 SOUR\n2 NAME gedcompy\n2 VERS {VERSION}\n1 CHAR UNICODE\n1 GEDC\n2 VERS 5.5\n2 FORM LINEAGE-LINKED\n0 @I1@ INDI\n1 SEX M\n0 @F2@ FAM\n0 TRLR"
    )

    assert (
        repr(gedcomfile)
        == f"GedcomFile(\nElement(0, 'HEAD', [Element(1, 'SOUR', [Element(2, 'NAME', 'gedcompy'), Element(2, 'VERS', '{VERSION}')]), Element(1, 'CHAR', 'UNICODE'), Element(1, 'GEDC', [Element(2, 'VERS', '5.5'), Element(2, 'FORM', 'LINEAGE-LINKED')])]),\nIndividual(0, 'INDI', '@I1@', [Element(1, 'SEX', 'M')]),\nFamily(0, 'FAM', '@F2@'),\nElement(0, 'TRLR'))"
    )


def test_can_only_add_indivisal_or_family_to_file():
    gedcomfile = gedcom.GedcomFile()
    title = gedcom.Element(tag="TITL")

    with pytest.raises(Exception):
        gedcomfile.add_element(title)


def test_can_add_indivisual_raw():
    gedcomfile = gedcom.GedcomFile()
    element = gedcom.Element(tag="INDI")
    gedcomfile.add_element(element)


def test_can_add_family_raw():
    gedcomfile = gedcom.GedcomFile()
    element = gedcom.Element(tag="FAM")
    gedcomfile.add_element(element)


def test_can_add_individual_obj():
    gedcomfile = gedcom.GedcomFile()
    element = gedcom.Individual()
    gedcomfile.add_element(element)


def test_can_add_family_obj():
    gedcomfile = gedcom.GedcomFile()
    element = gedcom.Family()
    gedcomfile.add_element(element)


def test_individual_ids_work():
    gedcomfile = gedcom.GedcomFile()
    element1 = gedcom.Individual()
    element2 = gedcom.Individual()
    assert element1.id is None
    assert element2.id is None

    gedcomfile.add_element(element1)
    gedcomfile.add_element(element2)

    assert element1.id == "@I1@"
    assert element2.id == "@I2@"


def test_id_assisment_is_robust():
    gedcomfile = gedcom.parse_string(
        "0 HEAD\n0 @I1@ INDI\n1 NAME\n2 GIVN Bob\n2 SURN Cox\n\n0 TRLR"
    )
    element1 = gedcom.Individual()

    assert element1.id is None

    gedcomfile.add_element(element1)

    assert element1.id == "@I2@"


def test_can_auto_detect_input_FP():
    fp = six.StringIO(GEDCOM_FILE)
    parsed = gedcom.parse(fp)
    assert isinstance(parsed, gedcom.GedcomFile) is True


def test_can_auto_detect_input_string():
    parsed = gedcom.parse(GEDCOM_FILE)
    assert isinstance(parsed, gedcom.GedcomFile) is True


def test_can_auto_detect_input_filename():
    myfile = tempfile.NamedTemporaryFile()
    filename = myfile.name

    parsed = gedcom.parse(filename)

    assert isinstance(parsed, gedcom.GedcomFile) is True


def test_support_name_in_given_and_surname():

    gedcomfile = gedcom.parse_string(
        "0 HEAD\n0 @I1@ INDI\n1 NAME\n2 GIVN Bob\n2 SURN Cox\n\n0 TRLR"
    )

    assert gedcomfile["@I1@"].name == ("Bob", "Cox")


def test_support_name_in_one_with_slashes():
    gedcomfile = gedcom.parse_string("0 HEAD\n0 @I1@ INDI\n1 NAME Bob /Cox/\n\n0 TRLR")
    assert gedcomfile["@I1@"].name == ("Bob", "Cox")


def test_save_file():

    gedcomfile = gedcom.parse_string(GEDCOM_FILE)
    outputfile = tempfile.NamedTemporaryFile()
    outputfilename = outputfile.name
    gedcomfile.save(outputfile)
    outputfile.seek(0, 0)

    assert outputfile.read() == GEDCOM_FILE.encode("utf8")
    with pytest.raises(
        Exception,
    ):
        gedcomfile.save(outputfilename)
    outputfile.close()

    gedcomfile.save(outputfilename)
    with open(outputfilename) as output:
        assert output.read() == GEDCOM_FILE
    remove(outputfilename)


def test_error_with_bad_tag():
    with pytest.raises(
        Exception,
    ):
        gedcom.Individual([], {"tag": "FAM"})


def test_error_with_bad_level():
    with pytest.raises(
        Exception,
    ):
        individual = gedcom.Individual(level="foo")
        individual.set_levels_downward


def test_note():
    gedcomfile = gedcom.parse_string(
        "0 HEAD\n0 @I1@ INDI\n1 NAME\n2 GIVN Bob\n2 SURN Cox\n1 NOTE foo\n0 TRLR"
    )
    assert list(gedcomfile.individuals)[0].note == "foo"


def test_note_cont():
    gedcomfile = gedcom.parse_string(
        "0 HEAD\n0 @I1@ INDI\n1 NAME\n2 GIVN Bob\n2 SURN Cox\n1 NOTE foo\n2 CONT bar\n0 TRLR"
    )
    assert list(gedcomfile.individuals)[0].note == "foo\nbar"


def tst_note_cont():
    gedcomfile = gedcom.parse_string(
        "0 HEAD\n0 @I1@ INDI\n1 NAME\n2 GIVN Bob\n2 SURN Cox\n1 NOTE foo\n2 CONT bar\n0 TRLR"
    )

    assert list(gedcomfile.individuals)[0].note == "foo\nbar"


def test_note_conc():
    gedcomfile = gedcom.parse_string(
        "0 HEAD\n0 @I1@ INDI\n1 NAME\n2 GIVN Bob\n2 SURN Cox\n1 NOTE foo\n2 CONC bar\n0 TRLR"
    )

    assert list(gedcomfile.individuals)[0].note == "foobar"


def test_note_error():
    gedcomfile = gedcom.parse_string(
        "0 HEAD\n0 @I1@ INDI\n1 NAME\n2 GIVN Bob\n2 SURN Cox\n1 NOTE foo\n2 TITL bar\n0 TRLR"
    )
    ind = list(gedcomfile.individuals)[0]

    with pytest.raises(ValueError):
        lambda: ind.note


def test_birth():
    gedcomfile = gedcom.parse_string(
        "0 HEAD\n0 @I1@ INDI\n1 NAME\n2 GIVN Bob\n2 SURN Cox\n1 BIRT\n2 DATE 1980\n2 PLAC London\n0 TRLR"
    )
    ind = list(gedcomfile.individuals)[0]
    birth = ind.birth

    assert birth.place == "London"
    assert birth.date == "1980"


def test_death():
    gedcomfile = gedcom.parse_string(
        "0 HEAD\n0 @I1@ INDI\n1 NAME\n2 GIVN Bob\n2 SURN Cox\n1 DEAT\n2 DATE 1980\n2 PLAC London\n0 TRLR"
    )
    ind = list(gedcomfile.individuals)[0]
    death = ind.death

    assert death.place == "London"
    assert death.date == "1980"


@pytest.mark.parametrize("sex", ["foo", "female", "male"])
def test_set_sex(sex):
    gedcomfile = gedcom.GedcomFile()
    ind = gedcomfile.individual()
    ind.set_sex("m")
    ind.set_sex("M")
    ind.set_sex("f")
    ind.set_sex("F")

    with pytest.raises(TypeError):
        ind.set_sex(sex)


def test_title():
    gedcomfile = gedcom.parse_string(
        "0 HEAD\n0 @I1@ INDI\n1 NAME\n2 GIVN Bob\n2 SURN Cox\n1 TITL King\n0 TRLR"
    )
    assert list(gedcomfile.individuals)[0].title == "King"

    gedcomfile = gedcom.parse_string(
        "0 HEAD\n0 @I1@ INDI\n1 NAME\n2 GIVN Bob\n2 SURN Cox\n0 TRLR"
    )
    assert list(gedcomfile.individuals)[0].title == None


def test_parse_error():
    with pytest.raises(Exception):
        gedcom.parse_string("foo")


def test_first_name_only():
    gedcomfile = gedcom.parse_string("0 HEAD\n0 @I1@ INDI\n1 NAME\n2 GIVN Bob\n0 TRLR")

    assert list(gedcomfile.individuals)[0].name == ("Bob", None)


def test_first_name_only_two():
    gedcomfile = gedcom.parse_string("0 HEAD\n0 @I1@ INDI\n1 NAME Bob\n0 TRLR")

    assert list(gedcomfile.individuals)[0].name == ("Bob", None)


def test_last_name_only():
    gedcomfile = gedcom.parse_string("0 HEAD\n0 @I1@ INDI\n1 NAME\n2 SURN Bob\n0 TRLR")

    assert list(gedcomfile.individuals)[0].name == (None, "Bob")


def test_empty_name():
    gedcomfile = gedcom.parse_string("0 HEAD\n0 @I1@ INDI\n1 NAME \n0 TRLR")

    assert list(gedcomfile.individuals)[0].name == (None, None)


def test_invalid_names():
    gedcomfile = gedcom.parse_string("0 HEAD\n0 @I1@ INDI\n1 NAME Bob /Russel\n0 TRLR")

    with pytest.raises(Exception):
        lambda: list(gedcomfile.individuals)[0].name


def test_dash_in_ID():
    gedcomfile = gedcom.parse_string(
        "0 HEAD\n0 @I1-123@ INDI\n1 NAME\n2 GIVN Bob\n0 TRLR"
    )

    assert list(gedcomfile.individuals)[0].name == ("Bob", None)
