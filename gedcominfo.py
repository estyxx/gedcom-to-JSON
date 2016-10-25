#!/usr/bin/python
# v. 0.1
# gedcamParseInfo
""" TODO: a persons ID and any information about that person. e.g. marriage, arrivals, etc. source ID, residence, etc."""

import gedcom
from datetime import datetime
import re
import sys

argIn = sys.argv[1]
# argOut = sys.argv[2]

def main():
    gedfile = gedcom.parse(argIn)

    # getPersonId(gedfile)
    # getIndiSource(gedfile)
    # getResidence(gedfile)
    # getArrivalEvent(gedfile)
    # getIndividualSource(gedfile)
    # getDivorceEvent(gedfile)
    # getBurialEvent(gedfile)
    # makeJSONobject(gedfile)
    # writeToJSONfile(gedfile)


"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
####################################################
# TODO:
# getArrivalEvent
# getIndividualSource
# getDivorceEvent
# getBurialEvent
# makeJSONobject
# writeToJSONfile
# second argument
####################################################
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""

def getPersonId(filename):
    """ get individual person ID """
    PiD = []
    for person in filename.individuals:
        PiD.append(person.id)
    return PiD

def getResidence(filename):
    """ get individual residence information """
    residenceDate = [] 
    residencePlace = []
    residenceSource = []
    residencePage = []
    for person in filename.individuals:
        try:
            residenceDate.append(person.residence.date)
        except IndexError:
            pass
    for person in filename.individuals:
        try:
            residencePlace.append(person.residence.place)
        except IndexError:
            pass
    for person in filename.individuals:
        try:
            residenceSource.append(person.residence.source.value)
        except IndexError:
            pass
    for person in filename.individuals:
        try:
            residencePage.append(person.residence.source.page)
        except IndexError:
            pass
        
    for i in residencePage:
        print i
        

def getIndiSource(filename):
    sourceId = []
    sourceRef = []
    for person in filename.individuals:
        try:
            sourceId.append(person.source.value)
        except IndexError:
            pass
    for person in filename.individuals:
        try:
            sourceRef.append(person.source.data.reference)
        except IndexError:
            pass

    for i in sourceRef:
        print i

def getSource(filename):
    # TODO
    pass

def getPage(filename):
    # TODO
    pass

def getArrivalEvent(filename):
    # TODO
    pass

def getBurialEvent(filename):
    # TODO
    pass

def getDivorceEvent(filename):
    # TODO
    pass

def getIndividualSource(filename):
    # TODO
    pass

def makeJSONobject(filename):
    # TODO
    pass

def writeToJSONfile(filename):
    # TODO
    pass

if __name__ == "__main__":
    main()
