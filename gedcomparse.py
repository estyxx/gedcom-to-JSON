#!/usr/local/bin/python

# import requirements for things to work
import gedcom
    # don't forget to build / install gedcompy for parsing
    ## in the gedcompy folder, run `python setup.py build && python setup.py install`
from datetime import datetime
from pytime import pytime
import re
import argparse

# parse for arguments from the command line. input/output files or help.
parser = argparse.ArgumentParser(description="Parse a *.gedcom file into *.json for use in FamilyGenie")
parser.add_argument('-i','--input', help='Input file name', required=True)
parser.add_argument('-o','--output', help='Output file name', required=True)
args = parser.parse_args()

def main():
    """
    the main function is the only function that runs when the program is called to run
    """
    ### parse gedcom file for information
    gedfile = gedcom.parse(args.input)
    ### file to write to 
    jsonfile = args.output
   
    ###  actual main function - makeJSONobject(gedfile)
    #  makeJSONobject(gedfile)
    writeToJSONfile(gedfile)
    
    ### test functions
    #  getAllInfo(gedfile)

    #  getName(gedfile)
    #  getSexAtBirth(gedfile)
    #  getBirthPlace(gedfile)
    #  getBirthDate(gedfile)
    #  getDeathDate(gedfile)
    #  getDeathPlace(gedfile)

    #  getBirth(gedfile)
    #  getDeath(gedfile)

    #  print parseTime(gedfile)
    #  print parseOutApprox(gedfile)

    
####################################################
# TODO: documentation
####################################################

#  TODO: in progress functions
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""

""" ########## STATIC functions for testing purposes #########"""

def getAllInfo(filename):
    """
    get all info unformatted
    """
    people = []
    # loop through each person in the file and add them to an array and return
    for person in filename.individuals:
        people.append(person)
    return people

def getBirth(filename):
    """
    get all birth records and print them to console
    """
    for person in filename.individuals:
        print person.birth

def getDeath(filename):
    """
    get all death records and print them to console
    """
    for person in filename.individuals:
        if person.death == None:
            pass
        else:
            try:
                print person.death.date
            except AttributeError:
                pass

""" ########## BUILDER functions for JSON files ######### """

def getBirthPlace(filename):
    """
    get all of the birth place records from the GEDCOM file
    """
    birthPlace = []
    for person in filename.individuals:
        try:
            if person.birth.place == None:
                birthPlace.append('"birthPlace" : "null"')
            else:
                birthPlace.append('"birthPlace" : "' + person.birth.place + '"')
        except AttributeError:
            birthPlace.append('"birthPlace" : "null"')
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
                birthDate.append('"birthDate" : "null"')
            else:
                birthDate.append('"birthDate" : "' + person.birth.date + '"')
        except AttributeError:
            birthDate.append('"birthDate" : "null"')
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
                deathPlace.append('"deathPlace" : "null"')
            else:
                deathPlace.append('"deathPlace" : "' + person.death.place + '"')
        except AttributeError:
            deathPlace.append('"deathPlace" : "null"')
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
            if person.death.date == None:
                deathDate.append('"deathDate" : "null"')
            else:
                deathDate.append('"deathDate" : "' + person.death.date + '"')
        except AttributeError:
            deathDate.append('"deathDate" : "null"')
    return deathDate

def getSexAtBirth(filename):
    """
    get the gender of a person from the GEDCOM file
    """
    sexAtBirth = []
    for person in filename.individuals:
        try:
            if person.sex == None:
                sexAtBirth.append('"sexAtBirth" : "null"')
            else:
                sexAtBirth.append('"sexAtBirth" : "' + person.sex + '"')
        except AttributeError:
            sexAtBirth.append('"sexAtBirth" : "null"')
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
            lastname = ''
        if firstname == None:
            firstname = ''
        firstName.append('"fName" : "' + firstname + '"')
        lastName.append('"lName" : "' + lastname + '"')
    return firstName, lastName

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

    birthDate = []
    deathDate = []
    bDate, dDate = parseOutApprox(filename)

    dateFormat = ['%m/%d/%Y', '%m-%d-%Y', '%d-%m-%Y', '%d, %b %Y', '%d %B %Y', '%d %b %Y', '%d %B, %Y', '%b %d, %Y', '%B %d, %Y', '%B %d %Y', '%b %d %Y', '%B %Y', '%b %Y', '%Y']

    for bd in bDate:
        if '\xe2\x80\x93' in bd:
            date1 = int(bd[:4])
            date2 = int(bd[-4:])
            avgDate = (date1+date2)/2
            birthDate.append('"birthDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxBirth" : "True"')
        elif '00000' in bd:
            birthDate.append('"birthDate" : "null",\n"approxBirth" : "False"')
        else:
            #  j = 0
            for i in dateFormat:
                try:
                    if i == '%Y':
                        birthDate.append('"birthDate" : "' + str(datetime.strptime(bd, i)) + '",\n"approxBirth" : "True"')
                        break
                    else:
                        birthDate.append('"birthDate" : "' + str(datetime.strptime(bd, i)) + '",\n"approxBirth" : "False"')
                        break
                except ValueError as e:
                    #  j += 1
                    #  print j, e
                    pass

    for dd in dDate:
        if '\xe2\x80\x93' in dd:
            date1 = int(dd[:4])
            date2 = int(dd[-4:])
            avgDate = (date1+date2)/2
            deathDate.append('"deathDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxDeath" : "True"')
        elif '00000' in dd:
            deathDate.append('"deathDate" : "null",\n"approxDeath" : "False"')
        else:
            #  j = 0
            for i in dateFormat:
                try:
                    if i == '%Y':
                        deathDate.append('"deathDate" : "' + str(datetime.strptime(dd, i)) + '",\n"approxDeath" : "True"')
                        break
                    else:
                        deathDate.append('"deathDate" : "' + str(datetime.strptime(dd, i)) + '",\n"approxDeath" : "False"')
                        break
                except ValueError as e:
                    #  j += 1 
                    #  print j, e
                    pass

    return birthDate, deathDate
    #  print len(birthDate), len(deathDate)
    #  for i, j in zip (birthDate, deathDate):
        #  print '\n',i,'\n\n',j,'\n'

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
        except AttributeError:
            bDate.append('00000')
   
    for person in filename.individuals:
        try:
            dDate.append(person.death.date)
        except AttributeError:
            dDate.append('00000')

    approx = {'About ': '','about ': '', 'ABT ': '', 'abt ': '', 'Abt ': '', 'abt. ': '', 'Abt. ': '', 'Bet. ': '', 'bet. ': '', 'Bet ': '', 'bet ': '', 'BEF ': '', 'Bef. ': '', 'bef. ': '', 'Bef ': '', 'bef ': '', 'Sept': 'sep'}

    for b in bDate:
        for i, j in approx.iteritems():
            b = b.replace(i,j)
        newbDate.append(b)
    
    for d in dDate:
        for i, j in approx.iteritems():
            d = d.replace(i,j)
        newdDate.append(d)

    #  print len(newbDate), len(newdDate)
    return newbDate, newdDate




def makeJSONobject(filename):
    """
    get information from the file, print and structure it in JSON
    """
    length = getAllInfo(filename)
    firstName, lastName = getName(filename)
    sexAtBirth = getSexAtBirth(filename)
    birthDate, deathDate = parseTime(filename)
    #  birthDate = getBirthDate(filename)
    birthPlace = getBirthPlace(filename)
    #  deathDate = getDeathDate(filename)
    deathPlace = getDeathPlace(filename)

    length = len(length)
    json = ''
    json += '[ \n'
    for i in range(length):
        json += '{ \n'
        json += firstName[i] + ',\n'
        json += lastName[i] + ',\n'
        json += sexAtBirth[i] + ',\n'
        json += birthDate[i] + ',\n'
        json += birthPlace[i] + ',\n'
        json += deathDate [i] + ',\n'
        json += deathPlace[i] + '\n'
        if i == (length - 1):
            json += '}\n'
        else:
            json += '},\n'
    json += ']'
    return json
    
    #  print "["
    #  for i in range(length):
        #  print "{"
        #  print firstName[i]
        #  print lastName[i]
        #  print sexAtBirth[i]
        #  print birthDate[i]
        #  print birthPlace[i]
        #  print deathDate[i]
        #  print deathPlace[i]
        #  if i == (length - 1):
            #  print "}"
        #  else:
            #  print "},"
    #  print "]"

def writeToJSONfile(filename):
    json = makeJSONobject(filename)
    f = open(args.output, "w")
    f.write(json)
    f.close()

if __name__ == "__main__":
    main()
