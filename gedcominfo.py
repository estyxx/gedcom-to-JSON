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

    #  getPersonId(gedfile)
    getNotes(gedfile)
    


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

def getNotes(filename):
    for person in filename.individuals:
        print person

def getSource(filename):
    # TODO
    pass

def getPage(filename):
    # TODO
    pass

def getResidence(filename):
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
