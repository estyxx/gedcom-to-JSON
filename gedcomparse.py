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
    #  parseTime(gedfile)
    #  monToNum(gedfile)
    parseOutApprox(gedfile)

    
####################################################

# TODO: in progress functions
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
def parseTime(filename):
    """
    formats timestamps into ISO time
    TODO
    """

    newDate = []
    for person in filename.individuals:
        try:
            if person.birth.date == None:
                pass
            else:
                pass
        except AttributeError:       
            pass
    for i in range(len(newDate)):
        if(newDate[i] == None):
            print "NO DATE RECORD"
        else:
            print pytime.parse(newDate[i])


def monToNum(filename):
    """
    Loop through records and replace months(as string), with months(as number)
    TODO: loop through records and month lists to replace all months with numbers, leaving exceptions for records that do not contain months as strings.
    """
    bDate = []
    for person in filename.individuals:
        try:
            bDate.append(person.birth.date)
        except AttributeError:
            pass
    
    for d in bDate:
        try:
            print datetime.strptime(d, '%m/%d/%Y')
        except ValueError:
            pass

def arrangeDate(filename):
    """
    TODO
    re-arrange dates to be formatted into ISO by PyTime
    """
    pass

def parseOutApprox(filename):
    """
    TODO
    remove 'abt', 'Abt', 'abt.', 'Abt.', 'Bet.', 'bet.', 'Bet', and 'bet' from dates.
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
   
    approx = {'abt ': '', 'Abt ': '', 'abt. ': '', 'Abt. ': '', 'Bet. ': '', 'bet. ': '', 'Bet ': '', 'bet ': ''}
    for b in bDate:
        for i, j in approx.iteritems():
            b = b.replace(i,j)
        newbDate.append(b)
    
    for d in dDate:
        for i, j in approx.iteritems():
            d = d.replace(i,j)
        newdDate.append(d)
    
    return newbDate, newdDate
    
    # TODO: loop through file and loop through approx list to replace any approx string with empty

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
