#!/usr/bin/python
# v. 0.3
# gedcamParseInfo
""" TODO: a persons ID and any information about that person. e.g. marriage, arrivals, etc. source ID, residence, etc."""

import gedcom
from datetime import datetime
import re
import sys

argIn = sys.argv[1]
argOut = sys.argv[2]

def main():
    gedfile = gedcom.parse(argIn)

    # parseTime(gedfile)
    # getPersonId(gedfile)
    # getIndiSource(gedfile)
    # getResidence(gedfile)
    # getResidenceDate(gedfile)
    # getEvent(gedfile)
    # getBurialDate(gedfile)
    # getBurialEvent(gedfile)
    # getDivorceEvent(gedfile)
    # makeJSONobject(gedfile)
    writeToJSONfile(gedfile)

"""''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
####################################################
# TODO:
# tests
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

    # initilaze lists
    residenceDate = []
    burialDate = []
    divorceDate = []
    eventDate = []

    # get the dates after the approximation strings have been removed
    rDate, bDate, dDate, eDate = parseOutApprox(filename)

    """
    dateFormat is used to loop through and check for what format the dates might be in
    if an error is thrown when running the file use the key from above and add the format to this list
    make sure that '%Y' is the last element of the list or everything breaks
    """
    dateFormat = ['%m/%d/%Y', '%m-%d-%Y', '%d-%m-%Y', '%d, %b %Y', '%d %B %Y', '%d %b %Y', '%d %B, %Y', '%b %d, %Y', '%B %d, %Y', '%B %d %Y', '%b %d %Y', '%B %Y', '%b %Y', '%m/%Y', '%Y']

    years = re.compile('^\d{4} \d{4} \d{4} .+')
     
    """ RESIDENCE DATE """
    for rd in rDate:
        if '\xe2\x80\x93' in rd or '-' in rd or ', ' in rd:
            # if there is a dash char in the date string that means the date was input as between date1 & date2. get the avg of these dates and use that
            date1 = int(rd[:4])
            date2 = int(rd[-4:])
            avgDate = (date1+date2)/2
            residenceDate.append('"residenceDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxResidence" : true,')
        elif years.match(rd):
            residenceDate.append('"residenceDate" : "' + str(datetime.strptime(str(rd[:4]), '%Y')) + '",\n"approxResidence" : true,')
        elif '00000' in rd:
            # if the date is stored as 00000 that means that it was not present while parsing through to remove the approximation strings
            residenceDate.append('"residenceDate" : null,\n"approxResidence" : false,')
        else:
            j = 0
            for i in dateFormat:
                try:
                    if i == '%Y':
                        # datetime.strptime is a public lib -- see the README. if the date does not match the date format string being tested, this function will error and exception will be passed
                        residenceDate.append('"residenceDate" : "' + str(datetime.strptime(rd, i)) + '",\n"approxResidence" : true,')
                        break
                    else:
                        residenceDate.append('"residenceDate" : "' + str(datetime.strptime(rd, i)) + '",\n"approxResidence" : false,')
                        break
                except ValueError as e:
                    j += 1
                    pass
            if j > len(dateFormat) -1:
                # if we have looped through all of the known date formats and haven't found a match, we will end up here, and this will throw an error.
                residenceDate.append('"residenceDate" : null,\n"approxResidence" : false,')
                print Exception(rd, "residenceDate - NEEDS MODIFICATION - check parseTime() or parseOutApprox() LINE {}".format(sys.exc_info()[-1].tb_lineno))

    """ BURIAL DATE """
    for bd in bDate:
        if '\xe2\x80\x93' in bd or '-' in bd or ', ' in bd:
            # if there is a dash char in the date string that means the date was input as between date1 & date2. get the avg of these dates and use that
            date1 = int(bd[:4])
            date2 = int(bd[-4:])
            avgDate = (date1+date2)/2
            burialDate.append('"burialDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxBurial" : true,')
        elif years.match(bd):
            burialDate.append('"burialDate" : "' + str(datetime.strptime(str(bd[:4]), '%Y')) + '",\n"approxBurial" : true,')
        elif '00000' in bd:
            # if the date is stored as 00000 that means that it was not present while parsing through to remove the approximation strings
            burialDate.append('"burialDate" : null,\n"approxBurial" : false,')
        else:
            j = 0
            for i in dateFormat:
                try:
                    if i == '%Y':
                        # datetime.strptime is a public lib -- see the README. if the date does not match the date format string being tested, this function will error and exception will be passed
                        burialDate.append('"burialDate" : "' + str(datetime.strptime(bd, i)) + '",\n"approxBurial" : true,')
                        break
                    else:
                        burialDate.append('"burialDate" : "' + str(datetime.strptime(bd, i)) + '",\n"approxBurial" : false,')
                        break
                except ValueError as e:
                    j += 1
                    pass
            if j > len(dateFormat) -1:
                # if we have looped through all of the known date formats and haven't found a match, we will end up here, and this will throw an error.
                burialDate.append('"burialDate" : null,\n"approxResidence" : false,')
                print Exception(bd, "burialDate - NEEDS MODIFICATION - check parseTime() or parseOutApprox() LINE {}".format(sys.exc_info()[-1].tb_lineno))

    """ DIVORCE DATE """
    for dd in dDate:
        if '\xe2\x80\x93' in dd or '-' in dd or ', ' in dd:
            # if there is a dash char in the date string that means the date was input as between date1 & date2. get the avg of these dates and use that
            date1 = int(dd[:4])
            date2 = int(dd[-4:])
            avgDate = (date1+date2)/2
            divorceDate.append('"divorceDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxDivorce" : true,')
        elif years.match(dd):
            divorceDate.append('"divorceDate" : "' + str(datetime.strptime(str(dd[:4]), '%Y')) + '",\n"approxDivorce" : true,')
        elif '00000' in dd:
            # if the date is stored as 00000 that means that it was not present while parsing through to remove the approximation strings
            divorceDate.append('"divorceDate" : null,\n"approxDivorce" : false,')
        else:
            j = 0
            for i in dateFormat:
                try:
                    if i == '%Y':
                        # datetime.strptime is a public lib -- see the README. if the date does not match the date format string being tested, this function will error and exception will be passed
                        divorceDate.append('"divorceDate" : "' + str(datetime.strptime(dd, i)) + '",\n"approxDivorce" : true,')
                        break
                    else:
                        divorceDate.append('"divorceDate" : "' + str(datetime.strptime(dd, i)) + '",\n"approxDivorce" : false,')
                        break
                except ValueError as e:
                    j += 1
                    pass
            if j > len(dateFormat) -1:
                # if we have looped through all of the known date formats and haven't found a match, we will end up here, and this will throw an error.
                divorceDate.append('"divorceDate" : null,\n"approxResidence" : false,')
                print Exception(dd, "divorceDate - NEEDS MODIFICATION - check parseTime() or parseOutApprox() LINE {}".format(sys.exc_info()[-1].tb_lineno))

    """ EVENT DATE """
    for ed in eDate:
        if '\xe2\x80\x93' in ed or '-' in ed or ', ' in ed:
            # if there is a dash char in the date string that means the date was input as between date1 & date2. get the avg of these dates and use that
            date1 = int(ed[:4])
            date2 = int(ed[-4:])
            avgDate = (date1+date2)/2
            eventDate.append('"eventDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxEvent" : true,')
        elif years.match(ed):
            eventDate.append('"eventDate" : "' + str(datetime.strptime(str(ed[:4]), '%Y')) + '",\n"approxEvent" : true,')
        elif '00000' in ed:
            # if the date is stored as 00000 that means that it was not present while parsing through to remove the approximation strings
            eventDate.append('"eventDate" : null,\n"approxEvent" : false,')
        else:
            j = 0
            for i in dateFormat:
                try:
                    if i == '%Y':
                        # datetime.strptime is a public lib -- see the README. if the date does not match the date format string being tested, this function will error and exception will be passed
                        eventDate.append('"eventDate" : "' + str(datetime.strptime(ed, i)) + '",\n"approxEvent" : true,')
                        break
                    else:
                        eventDate.append('"eventDate" : "' + str(datetime.strptime(ed, i)) + '",\n"approxEvent" : false,')
                        break
                except ValueError as e:
                    j += 1
                    pass
            if j > len(dateFormat) -1:
                # if we have looped through all of the known date formats and haven't found a match, we will end up here, and this will throw an error.
                eventDate.append('"eventDate" : null,\n"approxResidence" : false,')
                print Exception(ed, "eventDate - NEEDS MODIFICATION - check parseTime() or parseOutApprox() LINE {}".format(sys.exc_info()[-1].tb_lineno))

    return residenceDate, burialDate, divorceDate, eventDate

def parseOutApprox(filename):
    """
    remove approximation strings from dates.
    also fix four letter month names or make any other modifications to dates
    TODO: throw an error if there is an unknown approx string
    """

    """ get dates from input files """
    resiDate = getResidenceDate(filename)
    buriDate = getBurialDate(filename)
    divDate = getDivorceDate(filename)
    eventDate = getEventDate(filename)

    """ Declare lists """
    newResiDate = []
    newBuriDate = []
    newDivDate = []
    newEventDate = []


    """ Approximation RegExp to be removed """
    abt = re.compile('abt\.? ', re.IGNORECASE) # matches 'abt', possibly followed by a '.'
    bet = re.compile('bet\.? ', re.I) # matche 'bet', possibly followed by a '.'
    bef = re.compile('bef\.? ', re.I) # matches 'bef', possibly followed by a '.'
    sep = re.compile('sept', re.I) # matches 'sept'
    be = re.compile('before ', re.I) # matches 'about'
    a = re.compile('about ', re.I) # matches 'about'
    ea = re.compile('early ', re.I) # matches 'early'
    s = re.compile('(?<=\d)s') # matches an 's' preceded by a number - 1800(s)
    p = re.compile('\.(?= \d)') # matches a '.' followed by a space and a number - oct. 1995
    q = re.compile('\?') # matches a '?'

    # Once the records are stored locally parse out the approximation strings
    # loop through the records and the object with the replacements to find any and all replacements


    # loop through dates

    """ RESIDENCE DATE """
    for r in resiDate:
        r = abt.sub('', r)
        r = bet.sub('', r)
        r = bef.sub('', r)
        r = sep.sub('sep', r) # not removing approx -- changing the september month abbrev. sept is not a parseable month abbrev
        r = be.sub('', r)
        r = a.sub('', r)
        r = ea.sub('', r)
        r = s.sub('', r)
        r = p.sub('', r)
        r = q.sub('', r)

        newResiDate.append(r)

    """ BURIAL DATE """
    for b in buriDate:
        b = abt.sub('', b)
        b = bet.sub('', b)
        b = bef.sub('', b)
        b = sep.sub('sep', b) # not removing approx -- changing the september month abbrev. sept is not a parseable month abbrev
        b = be.sub('', b)
        b = a.sub('', b)
        b = ea.sub('', b)
        b = s.sub('', b)
        b = p.sub('', b)
        b = q.sub('', b)

        newBuriDate.append(b)

    """ DIVORCE DATE """
    for d in divDate:
        d = abt.sub('', d)
        d = bet.sub('', d)
        d = bef.sub('', d)
        d = sep.sub('sep', d) # not removing approx -- changing the september month abbrev. sept is not a parseable month abbrev
        d = be.sub('', d)
        d = a.sub('', d)
        d = ea.sub('', d)
        d = s.sub('', d)
        d = p.sub('', d)
        d = q.sub('', d)

        newDivDate.append(d)

    """ EVENT DATE """
    for e in eventDate:
        e = abt.sub('', e)
        e = bet.sub('', e)
        e = bef.sub('', e)
        e = sep.sub('sep', e) # not removing approx -- changing the september month abbrev. sept is not a parseable month abbrev
        e = be.sub('', e)
        e = a.sub('', e)
        e = ea.sub('', e)
        e = s.sub('', e)
        e = p.sub('', e)
        e = q.sub('', e)

        newEventDate.append(e)

    return newResiDate, newBuriDate, newDivDate, newEventDate

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
                    pass

                try:
                    sourceId.append('"personSourceId" : "' + source.value + '",')
                except AttributeError:
                    pass

                try:
                    sourcePage.append('"personSourcePage" : "' + source.page + '"')
                except AttributeError:
                    pass

                try:
                    sourceRef.append('"personSourceRef" : "' + source.data + '"')
                except AttributeError:
                    pass
        except AttributeError:
            # pass if no source information exists whatsoever for a person, we don't care if it doesn't exist
            pass

    return personSourceId, sourceId, sourceRef, sourcePage

def getResidenceDate(filename):
    """
    get the dates of residnce to be parsed into ISO format.

    :returns: residence dates as strings in a list
    :rtype: list
    """
    personId = []
    residenceDate = []

    # loop through all individuals and only store the people that have this type of information
    for person in filename.individuals:
        # get the peopele with residence records
        for residence in person.residence:
            try:
                personId.append(residence.parent.id)
            except AttributeError:
                # pass because we don't care if an individual doesn't have this type of information
                pass

    for pid in personId:
        for residence in person.get_by_id(pid).residence:
            try:
                residenceDate.append(residence.date)
            except AttributeError:
                residenceDate.append('00000')

    return residenceDate
    
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
    residenceInfo = []
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

        # `get_by_id` is built into gedcompy and return the object with the given Id
        for residence in person.get_by_id(pid).residence:
            personResidenceId.append('"personId" : "' + pid + '",')
            try:
                residenceInfo.append('"residenceInfo" : "' + residence.value + '",')
            except TypeError:
                residenceInfo.append('"residenceInfo" : null')
            try:
                residencePlace.append('"residencePlace" : "' + residence.place + '",')
            except AttributeError:
                residencePlace.append('"residencePlace" : null,')

            for source in residence.source:
                try:
                    residenceSource.append('"residenceSource" : "' +source.value + '",')
                except AttributeError:
                    residenceSource.append('"residenceSource" : null,')

                try:
                    residencePage.append('"residencePage" : "' + source.page + '"')
                except AttributeError:
                    residencePage.append('"residencePage" : null')

    return personResidenceId, residenceInfo, residencePlace, residenceSource, residencePage

def getEventDate(filename):
    """
    get event dates to be parsed into ISO time 

    :returns: event dates as strings in a list
    :rtype: list
    """
    eventDate = []
    personId = []

    # loop through all individuals and stores those who have this type of information
    for person in filename.individuals:
        for event in person.happening:
            try:
                personId.append(event.parent.id)
            except AttributeError:
                # pass because we don't care about the people who don't have this type of information
                pass

    for pid in personId:
        for event in person.get_by_id(pid).happening:
            try:
                eventDate.append(event.date)
            except AttributeError:
                eventDate.append('00000')
                
    return eventDate

def getEvent(filename):
    """
    get any extraneous events that a person might have (possibly incomplete)
    :TODO: handle multiple source information

    :returns: lists of various event information
    :rtype: list
    """

    # declare lists of information to be returned
    personId = []
    personEventId = []
    eventType = []
    eventInfo = []
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

        # `get_by_id` is built into gedcompy 
        for event in person.get_by_id(pid).happening:

            personEventId.append('"personId" : "' + pid + '",')

            try:
                eventType.append('"eventType" : "' + event.type + '",')
            except AttributeError:
                eventType.append('"eventType" : null,')

            try:
                eventPlace.append('"eventPlace" : "' + event.place + '",')
            except AttributeError:
                eventPlace.append('"eventPlace" : null,')

            try:
                eventInfo.append('"eventInfo" : "' + event.value + '",')
            except TypeError:
                eventInfo.append('"eventInfo" : null')

            for source in event.source:

                try:
                    eventSourceId.append('"eventSourceId" : "' + source.value + '",')
                except AttributeError:
                    eventSourceId.append('"eventSourceId" : null')

                try:
                    eventSourcePage.append('"eventSourcePage" : "' + source.page + '"')
                except AttributeError:
                    eventSourcePage.append('"eventSourcePage" : null')

    return personEventId, eventType, eventPlace, eventInfo, eventSourceId, eventSourcePage

def getBurialDate(filename):
    """
    get burial dates to be parsed into ISO time

    :returns: burial dates as strings in a list
    :rtype: list
    """
    burialDate = []
    for person in filename.individuals:
        if person.burial == None:
            pass
        else:
            try:
                burialDate.append(person.burial.date)
            except AttributeError:
               burialDate.append('00000') 

    return burialDate

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
                personBurialId.append('"personBurialId" : null')

            try:
                burialPlace.append('"burialPlace" : "' + person.burial.place + '",')
            except AttributeError:
                burialPlace.append('"burialPlace" : null')

            for source in person.burial.source:
                try:
                    burialSourceId.append('"burialSource" : "' + source.value + '"')
                except AttributeError:
                    burialSourceId.append('"burialSource" : null')

    return personBurialId, burialPlace, burialSourceId

def getDivorceDate(filename):
    """
    get divorce dates to be parsed into ISO time

    :returns: divorce dates as strings in a list
    :rtype: list
    """
    divorceDate = []
    for person in filename.individuals:
        try:
            for divorce in person.divorce:
                try:
                    divorceDate.append(divorce.date)
                except AttributeError:
                    divorceDate.append('00000')
        except AttributeError:
            pass

    return divorceDate

def getDivorceEvent(filename):
    """
    get any divorce information for an individual
    :TODO: handle multiple source information

    :returns: lists of divorce information
    :rtype: list
    """

    # declare lists to be returned
    personDivorceId = []
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
                    personDivorceId.append('"personDivorceId" : null,')

                try:
                    divorcePlace.append('"divorcePlace" : "' + divorce.place + '",')
                except AttributeError:
                    divorcePlace.append('"divorcePlace" : null,')

                for source in divorce.source:
                    try:
                        divorceSource.append('"sourceId" : "' + source.value + '",')
                    except AttributeError:
                        divorceSource.append('"sourceId" : null,')

                    try:
                        divorceSourceNote.append('"sourceNote" : "' + source.note + '",')
                    except AttributeError:
                        divorceSourceNote.append('"sourceNote " : null,')

                    try:
                        divorceSourceData.append('"sourceData" : "' + source.data + '"')
                    except AttributeError:
                        divorceSourceData.append('"sourceData" : null')

        except AttributeError:
            pass

    return personDivorceId, divorcePlace, divorceSource, divorceSourceNote, divorceSourceData

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
    residenceId, residenceInfo, residencePlace, residenceSource, residencePage = getResidence(filename)
    resiLength = len(residenceId)
    # Misc Events info
    personEventId, eventType, eventPlace, eventInfo, eventSourceId, eventSourcePage = getEvent(filename)
    eventLength = len(personEventId)
    # Burial info
    personBurialId, burialPlace, burialSourceId = getBurialEvent(filename)
    burialLength = len(personBurialId)
    # Divorce info
    personDivorceId, divorcePlace, divorceSource, divorceSourceNote, divorceSourceData = getDivorceEvent(filename)
    divorceLength = len(personDivorceId)
    # Date info
    residenceDate, burialDate, divorceDate, eventDate = parseTime(filename)
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
    personSource += '],'

    residence = ''
    residence += '[\n'
    for i in range(resiLength):
        residence += '{\n'
        residence += residenceId[i] + '\n'
        residence += residenceInfo[i] + '\n'
        residence += residenceDate[i] + '\n'
        residence += residencePlace[i] + '\n'
        residence += residenceSource[i] + '\n'
        residence += residencePage[i] + '\n'
        if i == (resiLength - 1):
            residence += '}\n'
        else:
            residence += '},\n'
    residence += '],'

    event = ''
    event += '[\n'
    for i in range(eventLength):
        event += '{\n'
        event += personEventId[i] + '\n' 
        event += eventType[i] + '\n'
        event += eventDate[i] + '\n'
        event += eventPlace[i] + '\n'
        event += eventInfo[i] + '\n'
        event += eventSourceId[i] + '\n'
        event += eventSourcePage[i] + '\n'
        if i == (eventLength - 1):
            event += '}\n'
        else:
            event += '},\n'
    event += '],'
    
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
    burial += '],'

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

    return personSource, residence, event, burial, divorce

def writeToJSONfile(filename):

    indiSource, resiSource, evenSource, buriSource, divSource = makeJSONobject(filename)
    f = open(argOut, "w") # create file
    f.writelines([indiSource,resiSource,evenSource,buriSource,divSource])
    f.close() # save file

if __name__ == "__main__":
    main()
