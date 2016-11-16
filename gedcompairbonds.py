#!/usr/bin/python
# v. 0.2
# gedcomParsePairBonds
"""
Parse a gedcom file into JSON for relationships between spouse
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
    writeToJSONfile(gedfile)

    #  getPartners(gedfile)
    #  getMarriageDate(gedfile)
    #  parseOutApprox(gedfile)
    #  parseTime(gedfile)
    #  print makeLength(gedfile)
    #  makeJSONobject(gedfile)

"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
####################################################
# TODO: docs
#       Tests
####################################################
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""

def getMarriageDate(filename):
   for family in filename.families:
       try:
           print family.marriage.date
       except IndexError:
           print "no marriage"
   
def getPartners(filename):
    """
    get the pid's of people in a marriage

    :returns: lists of husband and wife records
    :rtype: list
    """

    husband = []
    wife = []
    for marriage in filename.families:
        try:
            husband.append('"personOne_id" : "' + marriage.husband.value + '",\n')
        except AttributeError:
            husband.append('"personOne_id" : null,\n')
        try:
            wife.append('"personTwo_id" : "' + marriage.wife.value + '",\n')
        except AttributeError:
            wife.append('"personTwo_id" : null,\n')
    return husband, wife 

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

    # initilaze marriageDate lists
    marriageDate =[]

    # get the dates after the approximation strings have been removed
    mDate = parseOutApprox(filename)

    """
    dateFormat is used to loop through and check for what format the dates might be in
    if an error is thrown when running the file use the key from above and add the format to this list
    make sure that '%Y' is the last element of the list or everything breaks
    """
    dateFormat = ['%m/%d/%Y', '%m-%d-%Y', '%d-%m-%Y', '%d, %b %Y', '%d %B %Y', '%d %b %Y', '%d %B, %Y', '%b %d, %Y', '%B %d, %Y', '%B %d %Y', '%b %d %Y', '%B %Y', '%b %Y', '%m/%Y', '%Y']

    years = re.compile('^\d{4} \d{4} \d{4} .+') # for more than 2 years sequentially
    commayrs = re.compile('^\d{4}, \d{4}') # for years separated by a comma
    dashyrs = re.compile('^\d{4}-\d{4}') # for years separated by a dash 1998-1999

    for md in mDate:
        if '\xe2\x80\x93' in md or dashyrs.match(md) or commayrs.match(md):
            # if there is a dash char in the date string that means the date was input as between date1 & date2. get the avg of these dates and use that
            date1 = int(md[:4])
            date2 = int(md[-4:])
            avgDate = (date1+date2)/2
            marriageDate.append('"startDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxDate" : true')
        elif '00000' in md:
            # if the date is stored as 00000 that means that it was not present while parsing through to remove the approximation strings
            marriageDate.append('"startDate" : null,\n"approxDate" : false,\n')
        else:
            j = 0
            for i in dateFormat:
                try:
                    if i == '%Y':
                        # datetime.strptime is a public lib -- see the README. if the date does not match the date format string being tested, this function will error and exception will be passed
                        marriageDate.append('"startDate" : "' + str(datetime.strptime(md, i)) + '",\n"approxDate" : true')
                        break
                    else:
                        marriageDate.append('"startDate" : "' + str(datetime.strptime(md, i)) + '",\n"approxDate" : false')
                        break
                except ValueError as e:
                    j += 1
                    pass
            if j > len(dateFormat) -1:
                # if we have looped through all of the known date formats and haven't found a match, we will end up here, and this will throw an error.
                marriageDate.append('"startDate" : null,\n"approxDate" : false')
                print Exception(md, "startDate - NEEDS MODIFICATION - check parseTime() and parseOutApprox()")

    return marriageDate

def parseOutApprox(filename):
    """
    remove approximation strings from dates.
    also fix four letter month names or make any other modifications to dates
    TODO: throw an error if there is an unknown approx string
    """

    # first get all of the data from the input file
    # if there isn't one put 00000 as a placeholder to be replaced later
    marriageDate = []

    for family in filename.families:
        try:
            marriageDate.append(family.marriage.date)
        except AttributeError:
            marriageDate.append('00000')

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

    # initialize new marriagedate list
    newMarriageDate = []
    
    # loop through marriage dates
    for m in marriageDate:
        m = abt.sub('', m)
        m = bet.sub('', m)
        m = bef.sub('', m)
        m = sep.sub('sep', m) # not removing approx -- changing the september month abbrev. sept is not a parseable month abbrev
        m = be.sub('', m)
        m = a.sub('', m)
        m = e.sub('', m)
        m = s.sub('', m)
        m = p.sub('', m)
        m = q.sub('', m)

        # append parsed marriagedate to new marriage date list
        newMarriageDate.append(m)

    return newMarriageDate

def makeLength(filename):
    length = []
    for i in filename.families:
        length.append(i)
    return length

def makeJSONobject(filename):
    length = makeLength(filename)
    length = len(length)
    husband, wife = getPartners(filename)
    startDate = parseTime(filename)
    endDate = '"endDate" : null,\n'
    relType = '"relationshipType" : "Marriage",\n'

    json = ''
    json += '[ \n'
    for i in range(length):
        json += '{ \n'
        json += husband[i]
        json += wife[i]
        json += relType
        json += startDate[i]
        json += endDate
        json += '"user_id" : "' + userId + '"\n'
        if i == (length -1):
            json += '}\n'
        else:
            json += '},\n'
    json += ']'
    return json

def writeToJSONfile(filename):
    json = makeJSONobject(filename)
    f = open(argOut, "w")
    f.write(json)
    f.close()

if __name__ == "__main__":
    main()
