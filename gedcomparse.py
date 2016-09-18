import gedcom
    # don't forget to build / install gedcompy for parsing
from pytime import pytime
import re

def main():
    # parse gedcom file for information
    gedfile = gedcom.parse("GedComSample.ged")
    
    #  getName(gedfile)
    #  getSexAtBirth(gedfile)
    #  getBirthPlace(gedfile)
    #  getBirthDate(gedfile)
    #  getDeathDate(gedfile)
    #  getDeathPlace(gedfile)
    #  getBirth(gedfile)
    #  getDeath(gedfile)
    makeJSONobject(gedfile)
    #  parseTime(gedfile)
    
####################################################

"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
def parseTime(filename):
    """
    formats timestamps into ISO time
    """
    jan = re.compile('/jan/gi') # same for each month
    #  abt = re.compile('/abt\.?/gi') # same for between

    newDate = []
    for person in filename.individuals:
        try:
            if person.birth.date == None:
                pass
            else:
                newDate.append(person.birth.date.replace("abt ", '').replace("Bet. ",'').replace("Abt. ", ''))
        except AttributeError:       
            pass
    for i in range(len(newDate)):
        if(newDate[i] == None):
            print "NO DATE RECORD"
        else:
            print pytime.parse(newDate[i])
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""


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

def getBirthPlace(filename):
    """
    get all of the birth place records
    store them as a lists?
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
    get all of the birth place records
    store them as a lists?
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
    deathDate = []
    for person in filename.individuals:
        try:
            deathDate.append("'deathDate' : '" + person.death.date + "',")
        except AttributeError:
            deathDate.append("'deathDate' : 'null',")
    return deathDate

def getSexAtBirth(filename):
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
    get information from the file, print and structure it in JSON.
    using functions
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
