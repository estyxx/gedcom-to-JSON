#!/usr/bin/python
# v. 0.1
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
from datetime import datetime
from gedcomdates import *
from parsedate import *
import gedcom
import re
import sys

argIn = sys.argv[1] # gedcom file input
# argOut = sys.argv[2] # json file output
# various event types, in no particular order. global.
attributes = ['event', 'birth', 'death', 'divorce', 'burial', 'residence', 'bar_mitzvah', 'bas_mitzvah', 'blessing', 'christening', 'adult_christening', 'confirmation', 'confirmation_lds', 'cremation', 'graduation', 'immigration', 'naturalization', 'will']

def main():
    gedfile = gedcom.parse(argIn)
    # getEvents(gedfile)
    # makeEventRecords(gedfile)
    # test(gedfile)
    # makeJSONobject(gedfile)
    writeToJSONfile(gedfile)

def test(filename):
    for person in filename.individuals:
        try:
            print getattr(person, 'bar_mitzvah')
        except AttributeError:
            pass

def makeEventRecords(filename):

    eventRecords = []

    for person in filename.individuals:
        for attribute in attributes:
            buildRecord = '{\n'
            try:
                buildRecord += '"personId" : "' + getattr(person, attribute).parent_id + '",\n'
                buildRecord += '"eventType" : "' + attribute + '",\n'
                try:
                    buildRecord += '"eventDate" : "' + str(parseDate(getattr(person, attribute).date)) + '",\n'
                except AttributeError:
                    buildRecord += '"eventDate" : null,\n'
                try:
                    buildRecord += '"eventPlace" : "' + getattr(person, attribute).place + '"\n'
                except AttributeError:
                    buildRecord += '"eventPlace" : null\n'
                buildRecord += "}"
                eventRecords.append(buildRecord)
            except AttributeError:
                pass

    return eventRecords

def makeJSONobject(filename):

    eventRecords = makeEventRecords(filename)
    jsonEvents = '['

    i = 0
    for event in eventRecords:
        if i == len(eventRecords) - 1:
            jsonEvents += event + '\n'
        else:
            jsonEvents += event + ',\n'
        i += 1

    jsonEvents += ']'

    return jsonEvents

def writeToJSONfile(filename):
    """write the created json object to the output file and save it"""

    json = makeJSONobject(filename)
    f = open(argOut, "w") # creat/open the output file
    f.write(json)
    f.close() # save
    logfile.close()

if __name__ == "__main__":
    main()
