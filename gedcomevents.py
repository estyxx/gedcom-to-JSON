#!/usr/bin/python
# v. 0.4
# gedcomParseEvents
"""
Strategy: Declare a set list of event types, loop through individuals in the Gedcom file, and get all existing event information for each person. Store the information in a json file, each object referring to an event

Schema:
{
person_id   : String,    # [person.id]
event_type  : String,    # [person.<eventAttr>]
event_date  : Date,      # Formatted: ISO, [person.<eventAttr>.date]
event_place : String,    # [person.<eventAttr>.place]
}
"""

import sys

import gedcom
from gedcomdates import *
from parsedate import *

argIn = sys.argv[1]  # gedcom file input
argOut = sys.argv[2]  # json file output

# various event types, in no particular order. global.
attributes = [
    "event",
    "birth",
    "death",
    "divorce",
    "burial",
    "residence",
    "bar_mitzvah",
    "bas_mitzvah",
    "blessing",
    "christening",
    "adult_christening",
    "confirmation",
    "confirmation_lds",
    "cremation",
    "graduation",
    "immigration",
    "naturalization",
    "will",
]


def main():
    gedfile = gedcom.parse(argIn)

    writeToJSONfile(gedfile)


def makeEventRecords(filename):
    """
    Loop through the file and create records for each event for each person.

    Loop through each person, and then through each type of event.
    Create a json style record for each record that exists

    PersonId and EventType will exist for every record, while the date and place may or may not exist.

    :returns: json formatted strings of event records
    :rtype: list
    """

    eventRecords = []

    for person in filename.individuals:
        for attribute in attributes:
            buildRecord = "{\n"
            try:
                buildRecord += (
                    '"personId" : "' + getattr(person, attribute).parent_id + '",\n'
                )
                buildRecord += '"eventType" : "' + attribute + '",\n'

                try:
                    buildRecord += (
                        '"eventDate" : "'
                        + str(parseDate(getattr(person, attribute).date))
                        + '",\n'
                    )
                except AttributeError:
                    buildRecord += '"eventDate" : null,\n'

                try:
                    buildRecord += (
                        '"eventPlace" : "' + getattr(person, attribute).place + '"\n'
                    )
                except AttributeError:
                    buildRecord += '"eventPlace" : null\n'

                buildRecord += "}"
                eventRecords.append(buildRecord)
            # AttributeError if the event type does not exist for that person
            except AttributeError:
                pass

    return eventRecords


def makeJSONobject(filename):
    """
    Create a json array from the compiled event records

    :returns: json array of event records
    :rtype: string
    """

    eventRecords = makeEventRecords(filename)
    jsonEvents = "["

    i = 0
    for event in eventRecords:
        if i == len(eventRecords) - 1:
            jsonEvents += event + "\n"
        else:
            jsonEvents += event + ",\n"
        i += 1

    jsonEvents += "]"

    return jsonEvents


def writeToJSONfile(filename):
    """write the created json object to the output file and save it"""

    json = makeJSONobject(filename)
    f = open(argOut, "w")  # creat/open the output file
    f.write(json)
    f.close()  # save
    # logfile.close()


if __name__ == "__main__":
    main()
