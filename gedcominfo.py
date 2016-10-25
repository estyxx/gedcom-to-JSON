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
    pass
    gedfile = gedcom.parse(argIn)

    # getPersonId(gedfile)
    # getNotes(gedfile)
    getResidence(gedfile)
    


"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
####################################################
# TODO: everything
####################################################
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""

def getPersonId(filename):
    """
    get individual person ID 
    """
    PiD = []
    for person in filename.individuals:
        PiD.append(person.id)
    return PiD

def getResidence(filename):
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
        

def getNotes(filename):
    # TODO
    pass

def getSource(filename):
    # TODO
    pass

def getPage(filename):
    # TODO
    pass

def getArrivalEvent(filename):
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
