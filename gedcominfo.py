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
    getEvent(gedfile)
    # getBurialEvent(gedfile)
    # getDivorceEvent(gedfile)
    # makeJSONobject(gedfile)
    # writeToJSONfile(gedfile)
    # tests(gedfile)

"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
####################################################
# TODO:
# docs
# tests
# make json object may need its for loops wrapped in try/catch for IndexError using personId as the length
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

##### TIME FORMATTING #####
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

    # initilaze birthDate/deathDate lists
    birthDate = []
    deathDate = []

    # get the dates after the approximation strings have been removed
    bDate, dDate = parseOutApprox(filename)

    """
    dateFormat is used to loop through and check for what format the dates might be in
    if an error is thrown when running the file use the key from above and add the format to this list
    make sure that '%Y' is the last element of the list or everything breaks
    """
    dateFormat = ['%m/%d/%Y', '%m-%d-%Y', '%d-%m-%Y', '%d, %b %Y', '%d %B %Y', '%d %b %Y', '%d %B, %Y', '%b %d, %Y', '%B %d, %Y', '%B %d %Y', '%b %d %Y', '%B %Y', '%b %Y', '%m/%Y', '%Y']

    for bd in bDate:
        if '\xe2\x80\x93' in bd:
            # if there is a dash char in the date string that means the date in the file is between date1 & date2. get the avg of these dates and use that. set the ApproxDate to true
            date1 = int(bd[:4])
            date2 = int(bd[-4:])
            avgDate = (date1+date2)/2
            birthDate.append('"birthDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxBirth" : "True"')
        elif '00000' in bd:
            # if the date is stored as 00000 that means that it did not exist while parsing through to remove the approximation strings
            birthDate.append('"birthDate" : "null",\n"approxBirth" : "False"')
        else:
            j = 0 # counter for error handling
            for i in dateFormat:
                # loop through the dateFarmats, try to parse the date - expect errors but if the counter goes beyond the length of dateFormat, then the date didn't match any known format strings.
                try:
                    if i == '%Y':
                        # datetime.strptime is a public lib -- see the README. if the date does not match the date format string being tested, this function will error and exception will be passed
                        birthDate.append('"birthDate" : "' + str(datetime.strptime(bd, i)) + '",\n"approxBirth" : "True"')
                        break
                    else:
                        birthDate.append('"birthDate" : "' + str(datetime.strptime(bd, i)) + '",\n"approxBirth" : "False"')
                        break
                except ValueError as e:
                    j += 1
                    pass
            if j > len(dateFormat) -1:
                # if we have looped through all of the known date formats and haven't found a match, we will end up here, and this will throw an error.
                birthDate.append('"birthDate" : "null",\n"approxBirth" : "False"')
                print Exception(bd, "birthDate - NEEDS MODIFICATION - check parseTime() and parseOutApprox()")
                

    for dd in dDate:
        if '\xe2\x80\x93' in dd:
            # if there is a dash char in the date string that means the date was input as between date1 & date2. get the avg of these dates and use that
            date1 = int(dd[:4])
            date2 = int(dd[-4:])
            avgDate = (date1+date2)/2
            deathDate.append('"deathDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxDeath" : "True"')
        elif '00000' in dd:
            # if the date is stored as 00000 that means that it was not present while parsing through to remove the approximation strings
            deathDate.append('"deathDate" : "null",\n"approxDeath" : "False"')
        else:
            j = 0
            for i in dateFormat:
                try:
                    if i == '%Y':
                        # datetime.strptime is a public lib -- see the README. if the date does not match the date format string being tested, this function will error and exception will be passed
                        deathDate.append('"deathDate" : "' + str(datetime.strptime(dd, i)) + '",\n"approxDeath" : "True"')
                        break
                    else:
                        deathDate.append('"deathDate" : "' + str(datetime.strptime(dd, i)) + '",\n"approxDeath" : "False"')
                        break
                except ValueError as e:
                    j += 1
                    pass
            if j > len(dateFormat) -1:
                # if we have looped through all of the known date formats and haven't found a match, we will end up here, and this will throw an error.
                deathDate.append('"deathDate" : "null",\n"approxDeath" : "False"')
                print Exception(dd, "deathDate - NEEDS MODIFICATION - check parseTime() and parseOutApprox()")

    return birthDate, deathDate

def parseOutApprox(filename):
    """
    remove approximation strings from dates.
    also fix four letter month names or make any other modifications to dates
    TODO: throw an error if there is an unknown approx string
    """

    # first get all of the data from the input file
    # if there isn't one put 00000 as a placeholder to be replaced later
    bDate = []
    dDate = []

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

    # initialize new birthdate/deathdate list
    newbDate = []
    newdDate = []


    # loop through birth dates
    for b in bDate:
        b = abt.sub('', b)
        b = bet.sub('', b)
        b = bef.sub('', b)
        b = sep.sub('sep', b) # not removing approx -- changing the september month abbrev. sept is not a parseable month abbrev
        b = be.sub('', b)
        b = a.sub('', b)
        b = e.sub('', b)
        b = s.sub('', b)
        b = p.sub('', b)
        b = q.sub('', b)
        
        # append parsed birthdate to new birth date list
        newbDate.append(b)

    # loop through death dates
    for d in dDate:
        d = abt.sub('', d)
        d = bet.sub('', d)
        d = bef.sub('', d)
        d = sep.sub('sep', d) # not removing approx -- changing the september month abbrev. sept is not a parseable month abbrev
        d = be.sub('', d)
        d = a.sub('', d)
        d = e.sub('', d)
        d = s.sub('', d)
        d = p.sub('', d)
        d = q.sub('', d)

        # append parsed deathdate to new death date list
        newdDate.append(d)

    return newbDate, newdDate
##### END TIME #####

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
                    personSourceId.append('"personId" : "null",')

                try:
                    sourceId.append('"personSourceId" : "' + source.value + '",')
                except AttributeError:
                    sourceId.append('"personSourceId" : "null",')

                try:
                    sourcePage.append('"personSourcePage" : "' + source.page + '"')
                except AttributeError:
                    sourcePage.append('"personSourcePage" : "null"')

                try:
                    sourceRef.append('"personSourceRef" : "' + source.data + '"')
                except AttributeError:
                    sourceRef.append('"personSourceRef" : "null"')
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
    residenceDate = [] 
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
        personResidenceId.append('"personId" : "' + pid + '",')

        # `get_by_id` is built into gedcompy and return the object with the given Id
        for residence in person.get_by_id(pid).residence:
            try:
                residenceDate.append('"residenceDate" : "' + residence.date + '",')
            except AttributeError:
                residenceDate.append('"residenceDate" : "null",')

            try:
                residencePlace.append('"residencePlace" : "' + residence.place + '",')
            except AttributeError:
                residencePlace.append('"residencePlace" : "null",')

            for source in residence.source:
                try:
                    residenceSource.append('"residenceSource" : "' +source.value + '",')
                except AttributeError:
                    residenceSource.append('"residenceSource" : "null",')

                try:
                    residencePage.append('"residencePage" : ' + source.page + '"')
                except AttributeError:
                    residencePage.append('"residencePage" : "null"')


    return personResidenceId, residenceDate, residencePlace, residenceSource, residencePage

def getEvent(filename):
    """
    get any extraneous events that a person might have (possibly incomplete)
    :TODO: handle multiple source information
    
    :TODO: piece of info missing

    :returns: lists of various event information
    :rtype: list
    """

    # declare lists of information to be returned
    personId = []
    personEventId = []
    eventType = []
    eventInfo = []
    eventDate = []
    eventPlace = []
    eventSourceId = []
    eventSourcePage = []

    # loop through all individuals and stores those who have this type of information
    for person in filename.individuals:
        for event in person.happening:
            try:
                personId.append(event.parent.id)
            except AttributeError:
                # pass because we don't care about the people who don't have this type of information
                pass
            
    # loop through the people who have this type of information
    for pid in personId:
        personEventId.append('"personId" : "' + pid + '",')

        # `get_by_id` is built into gedcompy
        for event in person.get_by_id(pid).happening:

            try:
                eventType.append('"eventType" : "' + event.type + '",')
            except AttributeError:
                eventType.append('"eventType" : "null",')

            try:
                eventDate.append('"eventDate" : "' + event.date + '",')
            except AttributeError:
                eventDate.append('"eventDate" : "null",')

            try:
                eventPlace.append('"eventPlace" : "' + event.place + '",')
            except AttributeError:
                eventPlace.append('"eventPlace" : "null",')

            try:
                eventInfo.append('"eventInfo" : "' + event.value + '",')
            except AttributeError:
                eventInfo.append('"eventInfo" : "null"')

            for source in event.source:

                try:
                    eventSourceId.append('"eventSourceId" : "' + source.value + '",')
                except AttributeError:
                    eventSourceId.append('"eventSourceId" : "null"')

                try:
                    eventSourcePage.append('"eventSourcePage" : "' + source.page + '"')
                except AttributeError:
                    eventSourcePage.append('"eventSourcePage" : "null"')

    return personEventId, eventType, eventDate, eventPlace, eventInfo, eventSourceId, eventSourcePage

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
    burialDate = []
    burialSourceId = []

    # loop through all individuals in a file
    for person in filename.individuals:
        if (person.burial == None):
            # we don't care about people without any burial information
            pass

        else:
            try:
                personBurialId.append('"personBurialId" : "' + person.burial.parent.id + '",')
            except AttributeError:
                personBurialId.append('"personBurialId" : "null"')

            try:
                burialPlace.append('"burialPlace" : "' + person.burial.place + '",')
            except AttributeError:
                burialPlace.append('"burialPlace" : "null"')

            try:
                burialDate.append('"burialDate" : "' + person.burial.date + '",')
            except AttributeError:
                burialDate.append('"burialDate" : "null"')

            for source in person.burial.source:
                try:
                    burialSourceId.append('"burialSource" : "' + source.value + '"')
                except AttributeError:
                    burialSourceId.append('"burialSource" : "null"')

    return personBurialId, burialPlace, burialDate, burialSourceId

def getDivorceEvent(filename):
    """
    get any divorce information for an individual
    :TODO: handle multiple source information

    :returns: lists of divorce information
    :rtype: list
    """

    # declare lists to be returned
    personDivorceId = []
    divorceDate = []
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
                    personDivorceId.append('"personDivorceId" : "null",')

                try:
                    divorceDate.append('"divorceDate" : "' + divorce.date + '",')
                except AttributeError:
                    divorceDate.append('"divorceDate" : "null",')

                try:
                    divorcePlace.append('"divorcePlace" : "' + divorce.place + '",')
                except AttributeError:
                    divorcePlace.append('"divorcePlace" : "null",')

                for source in divorce.source:
                    try:
                        divorceSource.append('"sourceId" : "' + source.value + '",')
                    except AttributeError:
                        divorceSource.append('"sourceId" : "null",')

                    try:
                        divorceSourceNote.append('"sourceNote" : "' + source.note + '",')
                    except AttributeError:
                        divorceSourceNote.append('"sourceNote " : "null",')

                    try:
                        divorceSourceData.append('"sourceData" : "' + source.data + '"')
                    except AttributeError:
                        divorceSourceData.append('"sourceData" : "null"')

        except AttributeError:
            pass

    return personDivorceId, divorceDate, divorcePlace, divorceSource, divorceSourceNote, divorceSourceData

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
    residenceId, residenceDate, residencePlace, residenceSource, residencePage = getResidence(filename)
    resiLength = len(residenceId)
    # Misc Events info
    personEventId, eventType, eventDate, eventPlace, eventInfo, eventSourceId, eventSourcePage = getEvent(filename)
    eventLength = len(personEventId)
    # Burial info
    personBurialId, burialPlace, burialDate, burialSourceId = getBurialEvent(filename)
    burialLength = len(personBurialId)
    # Divorce info
    personDivorceId, divorceDate, divorcePlace, divorceSource, divorceSourceNote, divorceSourceData = getDivorceEvent(filename)
    divorceLength = len(personDivorceId)
    ### end access ###

    personSource = ''
    personSource += '[\n'
    for i in range(personLength):
        personSource += '{\n'
        personSource += personSourceId[i] + '\n'
        personSource += sourceId[i] + '\n'
        personSource += sourceRef[i] + '\n'
        personSource += sourcePage[i] + '\n'
        if i == (personLength - 1):
            personSource += '}\n'
        else:
            personSource += '},\n'
    personSource += ']'

    residence = ''
    residence += '[\n'
    for i in range(resiLength):
        residence += '{\n'
        residence += residenceId[i] + '\n'
        residence += residenceDate[i] + '\n'
        residence += residencePlace[i] + '\n'
        residence += residenceSource[i] + '\n'
        residence += residencePage[i] + '\n'
        if i == (resiLength - 1):
            residence += '}\n'
        else:
            residence += '},\n'
    residence += ']'

    event = ''
    event += '[\n'
    for i in range(eventLength):
        event += '{\n'
        event += personEventId[i] + '\n' 
        event += eventType[i] + '\n'
        event += eventDate[i] + '\n'
        event += eventPlace[i] + '\n'
        event += eventSourceId[i] + '\n'
        event += eventSourcePage[i] + '\n'
        if i == (eventLength - 1):
            event += '}\n'
        else:
            event += '},\n'
    event += ']'
    
    burial = ''
    burial += '[\n'
    for i in range(burialLength):
        burial += personBurialId[i] + '\n'
        burial += burialDate[i] + '\n'
        burial += burialPlace[i] + '\n'
        burial += burialSourceId[i] + '\n'
        if i == (burialLength - 1):
            burial += '}\n'
        else:
            burial += '},\n'
    burial += ']'

    divorce = ''
    divorce += '[\n'
    for i in range (divorceLength):
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

    print divorce
    return personSource, residence, event, burial, divorce

def writeToJSONfile(filename):
    # TODO
    # jsonfile.writelines([one,two,three,...])

    indiSource, resiSource, evenSource, buriSource, divSource = makeJSONobject(filename)
    f = open(argOut, "w") # create file
    f.writelines([indiSource,resiSource,evenSource,buriSource,divSource])
    f.close() # save file

    pass

if __name__ == "__main__":
    main()
