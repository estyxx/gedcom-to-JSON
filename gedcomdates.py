import gedcom
from datetime import datetime
import re
import sys

def parseOutApprox(filename, event):
    """
    Parse out approximations that are included in user input dates
    ex Abt. bet. About. etc

    :returns: dates in a list
    :rtype: list
    """

    dates = []
    print "dates init"

    for person in filename.individuals:
        try:
            dates.append(getattr(person, event).date)
        except AttributeError:
            dates.append('00000')
    print "after dates append"

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

    parsedDates = []
    print "parsed Dates init"

    # loop through dates
    for date in dates:
        date = abt.sub('', date)
        date = bet.sub('', date)
        date = bef.sub('', date)
        date = sep.sub('sep', date) # not removing approx -- changing the september month abbrev. sept is not a parseable month abbrev
        date = be.sub('', date)
        date = a.sub('', date)
        date = e.sub('', date)
        date = s.sub('', date)
        date = p.sub('', date)
        date = q.sub('', date)
        
        # append parsed birthdate to new birth date list
        parsedDates.append(date)
    print "after loop parsed dates"

    return parseTime(parsedDates)


def parseTime(dates):
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

    ISOdates = []
    "ISO dates init"

    dateFormat = ['%m/%d/%Y', '%m-%d-%Y', '%d-%m-%Y', '%d, %b %Y', '%d %B %Y', '%d %b %Y', '%d %B, %Y', '%b %d, %Y', '%B %d, %Y', '%B %d %Y', '%b %d %Y', '%B %Y', '%b %Y', '%m/%Y', '%Y']

    years = re.compile('^\d{4} \d{4} \d{4} .+') # for more than 2 years sequentially 1997 1998 1999 ...
    commayrs = re.compile('^\d{4}, \d{4}') # for years separated by a comma 1998, 1999
    dashyrs = re.compile('^\d{4}-\d{4}') # for years separated by a dash # 1998-1999
 
    print "after regex"

    for date in dates:
        if '\xe2\x80\x93' in date or dashyrs.match(date) or commayrs.match(date) :
            # if there is a dash char in the date string that means the date in the file is between date1 & date2. get the avg of these dates and use that. set the ApproxDate to true
            date1 = int(date[:4])
            date2 = int(date[-4:])
            avgDate = (date1+date2)/2
            ISOdates.append('"eventDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxDate" : "year"')
        elif '00000' in date:
            # if the date is stored as 00000 that means that it did not exist while parsing through to remove the approximation strings
            ISOdates.append('"eventDate" : null,\n"approxDate" : "exact"')
        elif years.match(date):
            ISOdates.append('"eventDate" : "' + str(datetime.strptime(str(rd[:4]), '%Y')) + '",\n"approxDate" : true,')
        else:
            j = 0 # counter for error handling
            for df in dateFormat:
                # loop through the dateFarmats, try to parse the date - expect errors but if the counter goes beyond the length of dateFormat, then the date didn't match any known format strings.
                try:
                    if df == '%Y':
                        # datetime.strptime is a public lib -- see the README. if the date does not match the date format string being tested, this function will error and exception will be passed
                        ISOdates.append('"eventDate" : "' + str(datetime.strptime(date, df)) + '",\n"approxDate" : "year"')
                        break
                    elif ( (df == '%B %Y') or (df == '%b %Y') or (df == '%m/%Y') ):
                        ISOdates.append('"eventDate" : "' + str(datetime.strptime(date, df)) + '",\n"approxDate" : "month"')
                    else:
                        ISOdates.append('"eventDate" : "' + str(datetime.strptime(date, df)) + '",\n"approxDate" : "exact"')
                        break
                except ValueError as e:
                    j += 1
                    pass
            if j > len(dateFormat) -1:
                # if we have looped through all of the known date formats and haven't found a match, we will end up here, and this will throw an error.
                ISOdates.append('"eventDate" : null,\n"approxDate" : "exact"')
                print Exception(date, "eventDate - NEEDS MODIFICATION - check parseTime() and parseOutApprox()")

    print "after date formatting"

    return ISOdates
