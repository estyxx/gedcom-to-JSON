#!/usr/bin/python
# v. 0.2
# gedcomParseParents
"""
Parse a gedcom file into JSON for relationships between parents and children.
Strategy: TODO
"""

# import requirements
import gedcom # don't forget to build/install
import sys
import re
from datetime import datetime

argIn = sys.argv[1]
argOut = sys.argv[2]
userId = sys.argv[3]

def main():

    gedfile = gedcom.parse(argIn)

    #  getFatherRelation(gedfile)
    #  getMotherRelation(gedfile)
    #  parseTime(gedfile)
    #  makeLength(gedfile)
    #  makeJSONobject(gedfile)
    writeToJSONfile(gedfile)
    

"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
####################################################
# TODO: docs
#       Tests
####################################################
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""

# note: AttributeError means that there are no records of that type for that person

def getFatherRelation(filename):
    """
    get father relations from the gedcom file and parse them into JSON

    # loop through people from the input file, store their father records and return the list
    :returns: father relation
    :rtype: list
    """
    fRel = []
    startDate = parseTime(filename)
    
    for person in filename.individuals:
        try:
            fRel.append('"child_id" : "' + person.id + \
                    '",\n"parent_id" : "' + person.father.id + '",\n' + \
                    '"relationshipType" : "Father",\n' + \
                    '"subType" : "Biological",\n')
        except AttributeError:
            fRel.append('"child_id" : "' + person.id + \
                    '",\n"parent_id" : null,\n'\
                    '"relationshipType" : "Father",\n' + \
                    '"subType" : null,\n')

    return fRel

def getMotherRelation(filename):
    """
    get mother relations from the input gedcom file and parse them into JSON

    # loop through people from the input file, store their mother records and return the list
    :returns: mother relations
    :rtype: list
    """
    mRel = []

    for person in filename.individuals:
        try:
            mRel.append('"child_id" : "' + person.id + \
                    '",\n"parent_id" : "' + person.mother.id + '",\n' + \
                    '"relationshipType" : "Mother",\n' + \
                    '"subType" : "Biological",\n')
        except TypeError as e:
            print e, person
        except AttributeError:
            mRel.append('"child_id" : "' + person.id + \
                    '",\n"parent_id" : null,\n'\
                    '"relationshipType" : "Mother",\n' + \
                    '"subType" : null,\n')

    return mRel

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

    %Y-%m-%d = 1995-06-28
    %m/%y/%d = 06/95/28
    %d %b %Y = 28 Jun 1995

    '\xe2\x80\x93' is a dash character (all 3 hex together represents a dash -- the full string)
    """

    # initilaze birthDate/newStartDate lists
    newStartDate = []

    # get the dates after the approximation strings have been removed
    startDate = parseOutApprox(filename)

    """
    dateFormat is used to loop through and check for what format the dates might be in
    if an error is thrown when running the file use the key from above and add the format to this list
    make sure that '%Y' is the last element of the list or everything breaks
    """
    dateFormat = ['%m/%d/%Y', '%m-%d-%Y', '%d-%m-%Y', '%d, %b %Y', '%d %B %Y', '%d %b %Y', '%d %B, %Y', '%b %d, %Y', '%B %d, %Y', '%B %d %Y', '%b %d %Y', '%B %Y', '%b %Y', '%m/%Y', '%Y']

    for sd in startDate:
        if '\xe2\x80\x93' in sd:
            # if there is a dash char in the date string that means the date was input as between date1 & date2. get the avg of these dates and use that
            date1 = int(sd[:4])
            date2 = int(sd[-4:])
            avgDate = (date1+date2)/2
            newStartDate.append('"startDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxDate" : true,\n')
        elif '00000' in sd:
            # if the date is stored as 00000 that means that it was not present while parsing through to remove the approximation strings
            newStartDate.append('"startDate" : null,\n"approxDate" : false,\n')
        else:
            j = 0
            for i in dateFormat:
                try:
                    if i == '%Y':
                        # datetime.strptime is a public lib -- see the README. if the date does not match the date format string being tested, this function will error and exception will be passed
                        newStartDate.append('"startDate" : "' + str(datetime.strptime(sd, i)) + '",\n"approxDate" : true,\n')
                        break
                    else:
                        newStartDate.append('"startDate" : "' + str(datetime.strptime(sd, i)) + '",\n"approxDate" : false,\n')
                        break
                except ValueError as e:
                    j += 1
                    pass
            if j > len(dateFormat) -1:
                # if we have looped through all of the known date formats and haven't found a match, we will end up here, and this will throw an error.
                newStartDate.append('"startDate" : null,\n"approxDate" : false')
                print Exception(sd, "startDate - NEEDS MODIFICATION - check parseTime() and parseOutApprox()")

    return newStartDate

def parseOutApprox(filename):
    """
    remove approximation strings from dates.
    also fix four letter month names or make any other modifications to dates
    TODO: throw an error if there is an unknown approx string
    """

    # first get all of the data from the input file
    # if there isn't one put 00000 as a placeholder to be replaced later
    startDate = []

    for person in filename.individuals:
        try:
            startDate.append(person.birth.date)
        except AttributeError:
            startDate.append('00000')

    """
    Approximation RegExp to be removed 
    """
    abt = re.compile('abt\.? ', re.IGNORECASE) # matches 'abt', possibly followed by a '.'
    bet = re.compile('bet\.? ', re.I) # matche 'bet', possibly followed by a '.'
    bef = re.compile('bef\.? ', re.I) # matches 'bef', possibly followed by a '.'
    sep = re.compile('sept', re.I) # matches 'sept'
    be = re.compile('before ', re.I) # matches 'about'
    a = re.compile('about ', re.I) # matches 'about'
    e = re.compile('early ', re.I) # matches 'early'
    s = re.compile('(?<=\d)s') # matches an 's' preceded by a number - 1800(s)
    p = re.compile('\.(?= \d)') # matches a '.' followed by a space and a number - oct. 1995
    q = re.compile('\?') # matches a '?'

    # Once the records are stored locally parse out the approximation strings
    # loop through the records and the object with the replacements to find any and all replacements

    # initialize new start list
    newStartDate = []


    # loop through dates
    for sd in startDate:
        sd = abt.sub('', sd)
        sd = bet.sub('', sd)
        sd = bef.sub('', sd)
        sd = sep.sub('sep', sd) # not removing approx -- changing the september month abbrev. sept is not a parseable month abbrev
        sd = be.sub('', sd)
        sd = a.sub('', sd)
        sd = e.sub('', sd)
        sd = s.sub('', sd)
        sd = p.sub('', sd)
        sd = q.sub('', sd)
        # append parsed date to new date list
        newStartDate.append(sd)

    return newStartDate

def makeLength(filename):
    """
    get all info unformatted
    """
    people = []
    # loop through each person in the file and add them to an list and return
    for person in filename.individuals:
        people.append(person)

    # loop through the the newly created list and print each record
    #  for person in people:
        #  print person

    # this is used for the length of the file
    return people

def makeJSONobject(filename):
    """
    create and format the json string

    :returns: json formatted string based on the previous functions
    :rtype: string
    """
    length = makeLength(filename)
    length = len(length)
    fRel = getFatherRelation(filename)
    mRel = getMotherRelation(filename)
    startDate = parseTime(filename)
    endDate = '"endDate" : null,\n'
    
    json = ''
    json += '[ \n'
    for i in range(length):
        json += '{\n'
        json += fRel[i]
        json += startDate[i]
        json += endDate
        json += '"user_id" : "' + userId + '"\n'
        json += '},\n{\n'
        json += mRel[i]
        json += startDate[i]
        json += endDate
        json += '"user_id" : "' + userId + '"\n'
        if i == (length - 1):
            json += '}\n'
        else:
            json += '},\n'
    json +=']'
    return json
        

def writeToJSONfile(filename):
    """
    write the created json object to the output file and save it
    """
    json = makeJSONobject(filename)
    f = open(argOut, "w") # create/open the output file
    f.write(json)
    f.close() # save

if __name__ == "__main__":
    main()
