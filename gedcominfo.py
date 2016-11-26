#!/usr/bin/python
# v. 0.3
# gedcamParseInfo
""" TODO: a persons ID and any information about that person. e.g. marriage, arrivals, etc. source ID, residence, etc."""

import gedcom
from datetime import datetime
from gedcomdates import *
import re
import sys

argIn = sys.argv[1]
argOut = sys.argv[2]

def main():
    gedfile = gedcom.parse(argIn)

    # parseTime(gedfile)
    # getPersonId(gedfile)
    # getIndiSource(gedfile)
    # getResidence(gedfile)
    # getResidenceDate(gedfile)
    # getEvent(gedfile)
    # getBurialDate(gedfile)
    # getBurialEvent(gedfile)
    # getDivorceEvent(gedfile)
    # makeJSONobject(gedfile)
    writeToJSONfile(gedfile)

"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
####################################################
# TODO:
# tests
# TODO: handle multiple source information, this may still produce logic errors which will result in incorrect source information for individuals
####################################################
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""

def getPersonId(filename):
    """ 
    get individual ID for every person in the file

    :returns: list of individual PiDs
    :rtype: list
    
    """
    PiD = []
    for person in filename.individuals:
        PiD.append(person.id)
    return PiD

def getIndiSource(filename):
    """ 
    get the source information for an individual, if it exists
    :TODO: handle multiple source information
    :TODO: only get individuals with source information, not those without. (`get_by_id` method)

    :returns: lists of each type of source information
    :rtype: list
    """
    # declare lists to be used
    personSourceId = []
    sourceId = []
    sourceRef = []
    sourcePage = []
    # loop through all individuals
    for person in filename.individuals:
        try:
            # loop through source information and add the json structure to a list
            for source in person.source:
                try:
                    personSourceId.append('"personId" : "' + source.parent.id + '",')
                except AttributeError:
                    pass

                try:
                    sourceId.append('"personSourceId" : "' + source.value + '",')
                except AttributeError:
                    pass

                try:
                    sourceRef.append('"personSourceRef" : "' + source.data + '",')
                except AttributeError:
                    pass

                try:
                    sourcePage.append('"personSourcePage" : "' + source.page + '"')
                except AttributeError:
                    pass

        except AttributeError:
            # pass if no source information exists whatsoever for a person, we don't care if it doesn't exist
            pass

    return personSourceId, sourceId, sourceRef, sourcePage

def getResidence(filename):
    """ 
    get individual residence information
    :TODO: handle multiple source information

    :returns: lists of individual residence information
    :rtype: list
    """
    # declare lists for the different types of information to be returned
    personId = []
    personResidenceId = []
    residenceInfo = []
    residencePlace = []
    residenceSource = []
    residencePage = []

    # loop through all individuals and only store the people that have this type of information
    for person in filename.individuals:
        # get the peopele with residence records
        for residence in person.residence:
            try:
                personId.append(residence.parent.id)
            except AttributeError:
                # pass because we don't care if an individual doesn't have this type of information
                pass

    # get the records for people that have them, by person id (pid)
    for pid in personId:

        # `get_by_id` is built into gedcompy and return the object with the given Id
        for residence in person.get_by_id(pid).residence:
            personResidenceId.append('"personId" : "' + pid + '",')
            try:
                residenceInfo.append('"residenceInfo" : "' + residence.value + '",')
            except TypeError:
                residenceInfo.append('"residenceInfo" : null,')
            try:
                residencePlace.append('"residencePlace" : "' + residence.place + '",')
            except AttributeError:
                residencePlace.append('"residencePlace" : null,')

            for source in residence.source:
                try:
                    residenceSource.append('"residenceSource" : "' +source.value + '",')
                except AttributeError:
                    residenceSource.append('"residenceSource" : null,')

                try:
                    residencePage.append('"residencePage" : "' + source.page + '"')
                except AttributeError:
                    residencePage.append('"residencePage" : null')

    return personResidenceId, residenceInfo, residencePlace, residenceSource, residencePage

def getEvent(filename):
    """
    get any extraneous events that a person might have (possibly incomplete)
    :TODO: handle multiple source information

    :returns: lists of various event information
    :rtype: list
    """

    # declare lists of information to be returned
    personId = []
    personEventId = []
    eventType = []
    eventInfo = []
    eventPlace = []
    eventSourceId = []
    eventSourcePage = []

    # loop through all individuals and stores those who have this type of information
    for person in filename.individuals:
        for event in person.event:
            try:
                personId.append(event.parent.id)
            except AttributeError:
                # pass because we don't care about the people who don't have this type of information
                pass
            
    # loop through the people who have this type of information
    for pid in personId:

        # `get_by_id` is built into gedcompy 
        for event in person.get_by_id(pid).event:

            personEventId.append('"personId" : "' + pid + '",')

            try:
                eventType.append('"eventType" : "' + event.type + '",')
            except AttributeError:
                eventType.append('"eventType" : null,')

            try:
                eventPlace.append('"eventPlace" : "' + event.place + '",')
            except AttributeError:
                eventPlace.append('"eventPlace" : null,')

            try:
                eventInfo.append('"eventInfo" : "' + event.value + '",')
            except TypeError:
                eventInfo.append('"eventInfo" : null,')

            for source in event.source:

                try:
                    eventSourceId.append('"eventSourceId" : "' + source.value + '",')
                except AttributeError:
                    eventSourceId.append('"eventSourceId" : null,')

                try:
                    eventSourcePage.append('"eventSourcePage" : "' + source.page + '"')
                except AttributeError:
                    eventSourcePage.append('"eventSourcePage" : null')

    return personEventId, eventType, eventPlace, eventInfo, eventSourceId, eventSourcePage

def getBurialEvent(filename):
    """
    get any burial event information for a person
    :TODO: handle multiple source information

    :returns: lists of burial information
    :rtype: list
    """

    # declare lists of information to be returned
    personBurialId = []
    burialPlace = []
    burialSourceId = []
    burialEventType = []

    # loop through all individuals in a file
    for person in filename.individuals:
        if (person.burial == None):
            # we don't care about people without any burial information
            pass

        else:
            try:
                personBurialId.append('"personId" : "' + person.burial.parent.id + '",')
            except AttributeError:
                personBurialId.append('"personId" : null,')

            try:
                burialPlace.append('"eventPlace" : "' + person.burial.place + '",')
            except AttributeError:
                burialPlace.append('"eventPlace" : null,')
            

            for source in person.burial.source:
                try:
                    burialSourceId.append('"eventSource" : "' + source.value + '",')
                except AttributeError:
                    burialSourceId.append('"eventSource" : null')

            burialEventType.append('"eventType" : "Burial"')

    return personBurialId, burialPlace, burialSourceId, burialEventType

def getDivorceEvent(filename):
    """
    get any divorce information for an individual
    :TODO: handle multiple source information

    :returns: lists of divorce information
    :rtype: list
    """

    # declare lists to be returned
    personDivorceId = []
    divorcePlace = []
    divorceSource = []
    divorceSourceNote = []
    divorceSourceData = []

    # loop through all individuals 
    for person in filename.individuals:

        try:
            # loop through the divorce information if it exists
            for divorce in person.divorce:

                try:
                    personDivorceId.append('"personDivorceId" : "' + divorce.parent.id + '",')
                except AttributeError:
                    personDivorceId.append('"personDivorceId" : null,')

                try:
                    divorcePlace.append('"divorcePlace" : "' + divorce.place + '",')
                except AttributeError:
                    divorcePlace.append('"divorcePlace" : null,')

                for source in divorce.source:
                    try:
                        divorceSource.append('"sourceId" : "' + source.value + '",')
                    except AttributeError:
                        divorceSource.append('"sourceId" : null,')

                    try:
                        divorceSourceNote.append('"sourceNote" : "' + source.note + '",')
                    except AttributeError:
                        divorceSourceNote.append('"sourceNote " : null,')

                    try:
                        divorceSourceData.append('"sourceData" : "' + source.data + '"')
                    except AttributeError:
                        divorceSourceData.append('"sourceData" : null')

        except AttributeError:
            pass

    return personDivorceId, divorcePlace, divorceSource, divorceSourceNote, divorceSourceData

def makeJSONobject(filename):
    """
    structure the information from previous functions into json
    
    :returns: json structured strings
    :rtype: string
    """

    ### access to each type of information from the previous funcitons and establish what to be looped through (person ID)###
    # Individual source info
    personSourceId, sourceId, sourceRef, sourcePage = getIndiSource(filename)
    personLength = len(personSourceId)
    # Residence info
    residenceId, residenceInfo, residencePlace, residenceSource, residencePage = getResidence(filename)
    resiLength = len(residenceId)
    # Misc Events info
    personEventId, eventType, eventPlace, eventInfo, eventSourceId, eventSourcePage = getEvent(filename)
    eventLength = len(personEventId)
    # Burial info
    personBurialId, burialPlace, burialSourceId, burialEventType = getBurialEvent(filename)
    burialLength = len(personBurialId)
    # Divorce info
    personDivorceId, divorcePlace, divorceSource, divorceSourceNote, divorceSourceData = getDivorceEvent(filename)
    divorceLength = len(personDivorceId)
    # Date info
    residenceDate = parseTime(filename, 'residence')
    burialDate = parseTime(filename, 'burial')
    divorceDate = parseTime(filename, 'divorce')
    eventDate = parseTime(filename, 'event')
    ### end access ###

    personSource = ''
    personSource += '[\n'
    for i in range(personLength):
        personSource += '{\n'
        personSource += personSourceId[i] + '\n'
        personSource += sourceId[i] + '\n'
        personSource += sourceRef[i] + '\n'
        personSource += sourcePage[i] + '\n'
        personSource += '},\n'

    residence = ''
    for i in range(resiLength):
        residence += '{\n'
        residence += residenceId[i] + '\n'
        residence += residenceInfo[i] + '\n'
        residence += residenceDate[i] + '\n'
        residence += residencePlace[i] + '\n'
        residence += residenceSource[i] + '\n'
        residence += residencePage[i] + '\n'
        residence += '},\n'

    event = ''
    for i in range(eventLength):
        event += '{\n'
        event += personEventId[i] + '\n' 
        event += eventType[i] + '\n'
        event += eventDate[i] + '\n'
        event += eventPlace[i] + '\n'
        event += eventInfo[i] + '\n'
        event += eventSourceId[i] + '\n'
        event += eventSourcePage[i] + '\n'
        event += '},\n'
    
    burial = ''
    for i in range(burialLength):
        burial += '{\n'
        burial += personBurialId[i] + '\n'
        burial += burialDate[i] + '\n'
        burial += burialPlace[i] + '\n'
        burial += burialSourceId[i] + '\n'
        burial += burialEventType[i] + '\n'
        if (divorceLength == 0) and (i == (burialLength -1)):
            burial += '}\n'
        else:
            burial += '},\n'

    divorce = ''
    for i in range (divorceLength):
        divorce += '{\n'
        divorce += personDivorceId[i] + '\n'
        divorce += divorceDate[i] + '\n'
        divorce += divorcePlace[i] + '\n'
        divorce += divorceSource[i] + '\n'
        divorce += divorceSourceNote[i] + '\n'
        divorce += divorceSourceData[i] + '\n'
        if i == (divorceLength - 1):
            divorce += '}\n'
        else:
            divorce += '},\n'
    divorce += ']'

    return personSource, residence, event, burial, divorce

def writeToJSONfile(filename):

    indiSource, resiSource, evenSource, buriSource, divSource = makeJSONobject(filename)
    f = open(argOut, "w") # create file
    f.writelines([indiSource,resiSource,evenSource,buriSource,divSource])
    f.close() # save file

if __name__ == "__main__":
    main()
