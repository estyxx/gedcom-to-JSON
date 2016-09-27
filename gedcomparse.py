#!/usr/local/bin/python

import gedcom
    # don't forget to build / install gedcompy for parsing
from datetime import datetime
from pytime import pytime
import re

def main():
    # parse gedcom file for information
    gedfile = gedcom.parse("GedComSample.ged")
   
    """
    actual main function - makeJSONobject(gedfile)
    """
    #  makeJSONobject(gedfile)
    
    #  getName(gedfile)
    #  getSexAtBirth(gedfile)
    #  getBirthPlace(gedfile)
    #  getBirthDate(gedfile)
    #  getDeathDate(gedfile)
    #  getDeathPlace(gedfile)
    #  getBirth(gedfile)
    #  getDeath(gedfile)

    parseTime(gedfile)
    #  monToNum(gedfile)
    #  parseOutApprox(gedfile)

    
####################################################

# TODO: in progress functions
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
def parseTime(filename):
    """
    formats timestamps into ISO time

    DATE FORMATTING KEY
    %y = two digit year : 97 | 78 | 65
    %Y = four digit year : 1997 | 1978 | 1842
    %m = one/two digit month : 01 | 3 | 11
    %b = (three letter) abbreviated month : Jan | feb | Dec
    %B = full month name : January | February | march
    %d = one/two digit day : 23 | 02 | 31
    """

    birthDate, deathDate = parseOutApprox(filename)

    dateFormat = ['%m/%d/%Y', '%m-%d-%Y', '%d-%m-%Y', '%d %B %Y', '%d %b %Y', '%b %d, %Y', '%B %d, %Y', '%b %d %Y', '%B %Y', '%b %Y', '%Y']

    for bd in birthDate:
        if '\xe2\x80\x93' in bd:
            date1 = int(bd[:4])
            date2 = int(bd[-4:])
            avgDate = (date1+date2)/2
            print datetime.strptime(str(avgDate), '%Y')
        else:
            for i in dateFormat:
                try:
                    print datetime.strptime(bd, i)
                except ValueError:
                    pass


def parseOutApprox(filename):
    """
    remove 'abt', 'Abt', 'abt.', 'Abt.', 'Bet.', 'bet.', 'Bet', and 'bet' from dates.
    also fix four letter month names or make any other modifications to dates
    """
    bDate = []
    dDate = []
    newbDate = []
    newdDate = []
    for person in filename.individuals:
        try:
            bDate.append(person.birth.date)
            dDate.append(person.death.date)
        except AttributeError:
            pass
   
    approx = {'abt ': '', 'Abt ': '', 'abt. ': '', 'Abt. ': '', 'Bet. ': '', 'bet. ': '', 'Bet ': '', 'bet ': '', 'Bef. ': '', 'bef. ': '', 'Bef ': '', 'bef ': '', 'Sept': 'sep'}

    for b in bDate:
        for i, j in approx.iteritems():
            b = b.replace(i,j)
        newbDate.append(b)
    
    for d in dDate:
        for i, j in approx.iteritems():
            d = d.replace(i,j)
        newdDate.append(d)

    return newbDate, newdDate

"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""




""" ########## STATIC functions for testing purposes #########"""
def getBirth(filename):
    """
    get all birth records and print them to console
    """
    for person in filename.individuals:
        if person.birth == None:
            pass
        else:
            print person.birth

def getDeath(filename):
    """
    get all death records and print them to console
    """
    for person in filename.individuals:
        if person.death == None:
            pass
        else:
            print person.death



""" ########## BUILDER functions for JSON files ######### """

def getBirthPlace(filename):
    """
    get all of the birth place records from the GEDCOM file
    """
    birthPlace = []
    for person in filename.individuals:
        try:
            if person.birth.place == None:
                pass
            else:
                birthPlace.append("'birthPlace' : '" + person.birth.place + "',")
        except AttributeError:
            birthPlace.append("'birthPlace' : 'null',")
    return birthPlace

def getBirthDate(filename):
    """
    get all of the birth date records from the GEDCOM file
    """
    #### yyyy-mm-dd #### reformatting ####
    birthDate = []
    for person in filename.individuals:
        try:
            if person.birth.date == None:
                pass
            else:
                birthDate.append("'birthDate' : '" + person.birth.date + "',")
        except AttributeError:
            birthDate.append("'birthDate' : 'null',")
    return birthDate

def getDeathPlace(filename):
    """
    get the death place from the GEDCOM file
    if it applies or exists
    """
    deathPlace = []
    for person in filename.individuals:
        try:
            if person.death.place == None:
                pass
            else:
                deathPlace.append("'deathPlace' : '" + person.death.place + "',")
        except AttributeError:
            deathPlace.append("'deathPlace' : 'null'")
    return deathPlace

def getDeathDate(filename):
    """
    get the static death date from the GEDCOM file
    dates from this are user input directly from the GEDCOM file and not uniformely formatted
    if it applies or exists
    """
    deathDate = []
    for person in filename.individuals:
        try:
            deathDate.append("'deathDate' : '" + person.death.date + "',")
        except AttributeError:
            deathDate.append("'deathDate' : 'null',")
    return deathDate

def getSexAtBirth(filename):
    """
    get the gender of a person from the GEDCOM file
    """
    sexAtBirth = []
    for person in filename.individuals:
        try:
            if person.sex == None:
                pass
            else:
                sexAtBirth.append("'sexAtBirth' : '" + person.sex + "',")
        except AttributeError:
            sexAtBirth.append("'sexAtBirth' : 'null',")
    return sexAtBirth

def getName(filename):
    """
    get the first and last name from the GEDCOM file
    """
    firstName = []
    lastName = []
    for person in filename.individuals:
        firstname, lastname = person.name
        if lastname == None:
            lastname = ""
        if firstname == None:
            firstname = ""
        firstName.append("'fName' : '" + firstname + "',")
        lastName.append("'lName' : '" + lastname + "',")
    return firstName, lastName




def makeJSONobject(filename):
    """
    get information from the file, print and structure it in JSON
    """
    firstName, lastName = getName(filename)
    sexAtBirth = getSexAtBirth(filename)
    birthDate = getBirthDate(filename)
    birthPlace = getBirthPlace(filename)
    deathDate = getDeathDate(filename)
    deathPlace = getDeathPlace(filename)
    print "["
    for i in range(len(deathDate)):
        print "{"
        print firstName[i]
        print lastName[i]
        print sexAtBirth[i]
        print birthDate[i]
        print birthPlace[i]
        print deathDate[i]
        print deathPlace[i]
        print "},"
    print "]"

if __name__ == "__main__":
    main()
