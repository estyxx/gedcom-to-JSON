#!/usr/bin/python
# v 0.1
# This DOES NOT handle missing dates

from datetime import datetime
import re, sys, os

def main ():
    pass

def parseDate(date):
    preFormat = removeApprox(date)
    isoDate = formatToISO(preFormat)
    return isoDate

def removeApprox(dateString):

    """
    Approximation RegExp to be removed
    """
    regexp = re.compile('abt\.? |bet\.? |bef\.? |before |about |early |(?<=\d)s|\?|\.', re.IGNORECASE)
    sept = re.compile('sept', re.IGNORECASE)
    newDate = sept.sub('sep', regexp.sub('', dateString))

    return newDate

def formatToISO(date):
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

    dateFormat = ['%m/%d/%Y', '%m-%d-%Y', '%d-%m-%Y', '%m %d %Y', '%d, %b %Y', '%d %B %Y', '%d %b %Y', '%d %B, %Y', '%b %d, %Y', '%B %d, %Y', '%B %d %Y', '%b %d %Y', '%Y, %b %d', '%Y %m %d', '%B %Y', '%b %Y', '%m/%Y', '%Y']
    years = re.compile('^\d{4} \d{4} \d{4} .+') # for more than 2 years sequentially 1997 1998 1999 ...
    commayrs = re.compile('^\d{4}, \d{4}') # for years separated by a comma 1998, 1999
    dashyrs = re.compile('^\d{4}-\d{4}') # for years separated by a dash # 1998-1999

    if '\xe2\x80\x93' in date or dashyrs.match(date) or commayrs.match(date):
        date1 = int(date[:4])
        date2 = int(date[-4:])
        avgDate = (date1+date2)/2
        ISODate = '"eventDate" : "' + str(datetime.strptime(str(avgDate), '%Y')) + '",\n"approxDate" : "year"'
        return ISODate

    elif years.match(date):
        ISODate = '"eventDate" : "' + str(datetime.strptime(str(rd[:4]), '%Y')) + '",\n"approxDate": "year"'
        return ISODate

    else:
        j = 0
        for df in dateFormat:
            try:
                if df == '%Y':
                    ISODate = '"eventDate" : "' + str(datetime.strptime(date,df)) + '",\n"approxDate" : "year"'
                    break
                elif ( (df == '%B %Y') or (df == '%b %Y') or (df == '%m/%Y') ):
                    ISODate = '"eventDate" : "' + str(datetime.strptime(date,df)) + '",\n"approxDate" : "month"'
                else:
                    ISODate = '"eventDate" : "' + str(datetime.strptime(date, df)) + '",\n"approxDate" : "exact"'
                    break
            except ValueError:
                j += 1
                pass
        if j > len(dateFormat) - 1:
            raise Exception, "Input Date Format Unknown: " + date
    return ISODate


if __name__ == "__main__":
    main()
