# GedcomParse
Parse JSON data out of a .gedcom file using gedcompy & python2.7

  
## Installation:
### Python
<a href="http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/"> Mac Installation </a> <br>
<a href="http://www.howtogeek.com/197947/how-to-install-python-on-windows/"> Windows Installation </a> <br>
<a href="http://docs.python-guide.org/en/latest/starting/install/linux/"> Linux Installation </a>
### GedcomPy

Download with this repository, and follow the installation steps.

###### I have made small but important changes to gedcompy, for specific use with this program.

##### Installation:

navigate into the gedcompy folder and install:

  `cd gedcompy` <br>
  `python setup.py build` <br>
  `python setup.py install` - may have to use sudo

### GedcomParse
##### For Local use:
Clone from this repository & move any .ged files into the GedComParse folder to be parsed into json.
##### Requirements
* `python2.7` : see above
* <a href='https://pypi.python.org/pypi/pip'>`pip`</a> (package installer python, included in python download)
* <a href='https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior'>`datetime`</a> (pip install datetime)
* `gedcompy` : see below
* `six` (pip install six)

##### Node Modules
* `child-process` - running python from node
* <a href='https://github.com/expressjs/multer'>`multer`</a> - for uploading files
* `body-parser`
* `express`
* `mongoose`
  
## Usage (from terminal):
* Move the gedcom file into the GedComParse folder for use.

Usage: 

`$ python gedcomparse.py INPUT_FILE.ged OUTPUT_FILE.json`

`$ python gedcomparent.py INPUT_FILE.ged OUTPUT_FILE.json`

`$ python gedcompairbonds.py INPUT_FILE.ged OUTPUT_FILE.json`

`$ python gedcominfo.py INPUT_FILE.ged OUTPUT_FILE.json`

> Parse a .gedcom file into .json for use in FamilyGenie


### gedcomparse.py
Parses out information for individual people in a gedcom file, into json. 

Attributes:

* First Name
* Last Name
* Sex
* Birth Date (and if the date is approximated)
* Birth Place
* Death Date (and if the date is approximated)
* Death Place
* Person Id


### gedcomparent.py
Parses out information for child / parent relationships. There are different records for each relationship, so each individual may have a separate record for each of their parent relationships. 

Attributes:

* Child Id
* Parent Id
* Relationship Type (father / mother)
* Sub Type (biological)
* Start Date (defaults to birthday of the child, and if that date is approximate)
* End Date

### gedcompairbonds.py
Parses out information for pair bond relationships. Any given person may have multiple relationships. Any given person may have a relationship where the second partner is not known.

Attributes:

* Person One Id
* Person Two Id
* Relationship Type
* Start Date (and if it's approximated)
* Sub Type
* End Date

### gedcominfo.py
Parses out any extraneous information about a person. Events, Source information, Residence information, etc.

Source Attributes: **

* Person Id
* Person Source Id
* Source Reference
* Source Page

Event Attributes:

* Person Id
* Event Type
* Event Date
* Event Place
* Event Info

Residence Attributes:

* Person Id
* Residence Information
* Residence Start Date (and if it's approximated)
* Residence Place
* Residence Source + Source Information **

Various Events Attributes:

* Person Id
* Event Type
* Event Date (and if it's approximated)
* Event Place
* Event Info
* Event Source + Source Information **

Burial Attributes:

* Person Id
* Burial Date (and if it's approximated)
* Burial Place
* Burial Source**

Divorce Attributes:

* Person Id
* Divorce Date (and if it's approximated)
* Divorce Place
* Divorce Source + Source Information **

><span style="color:black"> if the given file does not hold any particular record, `null` will be the value given</span>

###### ** Source information at this point is not reliable, and much of it could be incorrect.

## Usage (from Node server):
Multer (npm package) handles the uploads and places them in a folder.

exec (child_process, npm package) handles the execution of the python program in the terminal, from the node server without any additional work.

post to the 'uploads' folder (or wherever you like), and the `exec` function will run it through the parser, placing the result in another folder. 

```javascript
// multer options
var upload = multer({ dest : 'uploads/' });
// executable child process:
var exec = require('child_process').exec;
//run the process on post
app.post('/uploads', upload, 
    function(req,res,next) {
        // run the python parser on the gedcom file
        exec('python path/to/gedcomparse.py path/to/gedcom-file.ged path/to/new-json-file.json',
        function(err) {
            if(err) { 
                console.log(err); 
            }
            // then to put the files into mongo ...
            exec('mongoimport --db database --collection collection --type json --file path/to/json-file.json --jsonArray', 
                function(err) {
                    if(err) {
                        console.log(err);
                    }
            });
        });
    res.redirect('/');
});

```

gedcompy
========

Python library to parse and work with <a href='https://en.wikipedia.org/wiki/GEDCOM'>`GEDCOM`</a> (genealogy/family tree) files.

It's goal is to support GEDCOM v5.5 (<a href='http://homepages.rootsweb.ancestry.com/~pmcbride/gedcom/55gctoc.htm'>`Specification Here`</a>).

This is released under the GNU General Public Licence version 3 (or at your option, a later version). See the file `LICENCE` for more.

## gedcompy Usage:
gedcompy parses out the records of each person and stores them as nested objects, accesible through dot notation.

Example Usage
-------------
```python
    >>> import gedcom
    >>> gedcomfile = gedcom.parse("myfamilytree.ged")
    >>> for person in gedcomfile.individuals:
    ...    firstname, lastname = person.name
    ...    print "{0} {1} is in the file".format(firstname, lastname)
```

The file as a whole is a generator object.

```python
>>> import gedcom
>>> gedfile = gedcom.parse("myfamilytree.ged")
>>> print gedfile
# GedcomFile(Element(0, 'HEAD', [Element(1, 'CHAR', 'UTF-8'), Element(1, 'SOUR', 'Ancestry.com Family Trees', [Element(2, 'VERS', '(2010.3)'), Element(2, 'NAME', 'Ancestry.com Family Trees'), Element(2, 'CORP', 'Ancestry.com')]), Element(1, 'GEDC', [Element(2, 'VERS', '5.5'), Element(2, 'FORM', 'LINEAGE-LINKED')])]),
# Individual(0, 'INDI', '@P1@', [Birth(1, 'BIRT', [Element(2, 'DATE', '03 dec 1970')]), Element(1, 'SEX', 'M'), Element(1, 'NAME', 'John /Smith/'), Element(1, 'FAMC', '@F1@')])
# Individual(0, 'INDI', '@P2@', [Element(1, 'NAME', 'Jane /Doe/'), Element(1, 'SEX', 'M'), Birth(1, 'BIRT', [Element(2, 'DATE', '06 nov 1946'), Element(2, 'PLAC', 'Brooklyn, New York City, New York, USA')]), Element(1, 'FAMS', '@F1@')])
```

## Individuals ['INDI']
Cannot access individuals as a whole:

```python
>>> print gedfile.individuals
# <generator object <genexpr> at 0x103ef25a0>
>>> print gedfile.individual # Probably Don't.
# Don't do this. It prints all individual records in the file.
```

To access individual records:

```python
>>> for person in gedfile.individuals:
...     print person
# Individual(0, 'INDI', '@P1@', [Birth(1, 'BIRT', [Element(2, 'DATE', '03 dec 1970')]), Element(1, 'SEX', 'M'), Element(1, 'NAME', 'John /Smith/'), Element(1, 'FAMC', '@F1@')])
# Individual(0, 'INDI', '@P2@', [Element(1, 'NAME', 'Jane /Doe/'), Element(1, 'SEX', 'M'), Birth(1, 'BIRT', [Element(2, 'DATE', '06 nov 1946'), Element(2, 'PLAC', 'Brooklyn, New York City, New York, USA')]), Element(1, 'FAMS', '@F1@')])
```
To access individual records of a specific type use dot notation:

```python
>>> for person in gedfile.individuals:
...     print person.birth
# Birth(1, 'BIRT', [Element(2, 'DATE', '03 dec 1970')])
# Birth(1, 'BIRT', [Element(2, 'DATE', '06 nov 1946'), Element(2, 'PLAC', 'Brooklyn, New York City, New York, USA')])
```

To specify individual record types:

```python
>>> for person in gedfile.individuals:
...     print person.birth.date
# 03 dec 1970
# 06 nov 1946
>>> for person in gedfile.individuals:
...     print person.birth.place
# AttributeError: 'NoneType' object has no attribute 'value'
# this does not print: Brooklyn, New York City, New York, USA
```
The AttributeError is thrown when a record of that type does not exist, and by default will NOT pass onto the next record.


##### current available use cases
```
person.birth              # class - birth
person.birth.place        # string
person.birth.date         # string
person.death              # class - death
person.death.place        # string
person.death.date         # string
person.name               # tuple - firstname, lastname
person.father             # class - father
person.mother             # class - mother
person.parents            # list - contaning father and mother class
person.aka                # list - 'also known as' name
person.gender             # string - 'M' or 'F'
person.sex                # string - ''     ''
person.id                 # string - @P12@
person.is_female          # boolean
person.is_male            # boolean
person.note               # string
person.title              # string
person.default_tag        # string tagname : 'INDI', 'FAM', etc
person.tag                # string tagname : 'INDI', 'FAM', etc

```

#### Advanced usage

##### Person + Parents

```python
>>> for person in gedfile.individuals:
...     try:
...         print person.name, person.parents[0].name, person.parents[1].name
...     except IndexError:
...         print "no parent name record for this person"
# OR
>>> for person in gedfile.individual:
...     try:
...         print person.name, person.father.name, person.mother.name
...     except AttributeError:
...        print "no parent name record for this person"
# either one will print:
# ('John', 'Doe') ('Jack', 'Doe') ('Jane', 'Doe')
# ('Jenny', 'Doe') ('Jack', 'Doe') ('Jane', 'Doe')
```
##### get\_by\_id()
ex. only get people with event records.

```python
>>> personId = []
>>> for person in gedfile.individuals:
...     for event in person.happening:
...         try:
...             personId.append(event.parent.id)
...         except AttributeError:
...             pass # because we don't care about people that don't have event records
>>> for pid in personId:
...     print person.get_by_id(pid)
# prints an individual's records. 
```


## Families ['FAMC']/['FAMS']

Family records are accessed the same way as individuals

```python
>>> print gedfile.families
# <generator object <genexpr> at 0x10523c7d0>
>>> print gedfile.family # Probably don't.
# Don't do this. Prints all family records in the family
```

```python
>>> for family in gedfile.families:
...     print family
# Family(0, 'FAM', '@F1@', [Husband(1, 'HUSB', '@P5@'), Wife(1, 'WIFE', '@P1@'), Element(1, 'CHIL', '@P2@', [Element(2, '_FREL', 'Natural'), Element(2, '_MREL', 'Natural')])])

>>> for family in gedfile.families:
...     print family.partners
# [Husband(1, 'HUSB', '@P5@'), Wife(1, 'WIFE', '@P1@')]
```

Use cases for partners:

```python
>>> for family in gedfile.families:
...     print family.partners[0]
...     print family.partners[1]
# Husband(1, 'HUSB', '@P5@')
# Wife(1, 'WIFE', '@P1@')

>>> for family in gedfile.families:
...     print family.partners[0].tag
# HUSB

>>> for family in gedfile.families:
...     print family.partners[0].value
# @P5@

>>> for family in gedfile.families:
...     print family.husband
...     print family.wife
# Husband(1, 'HUSB', '@P5@')
# Wife(1, 'WIFE', '@P1@')
```

Use cases for children

##### current available use cases

```
family.id                       # string '@F49@'
family.tag                      # string 'FAM'
family.partners                 # list 
family.wife                     # class - wife
family.husband                  # class - husband
family.children                 # list
family.children.father_relation # String 'Natural'
family.children.mother_relation # string 'Natural'
```
## Sources

This gets into more deeply nested elements.
Sources can also be nested within an individuals element as well as recorded for the individual themself. 

```python
>>> for person in gedfile.individuals:
... 		print person.source
#  Source(1, 'SOUR', '@S-357352754@', [Page(2, 'PAGE', 'Ancestry Family Tree'), Data(2, 'DATA', [Reference(3, 'TEXT', 'http://trees.ancestry.com/pt/AMTCitationRedir.aspx?tid=12345678&pid=21')])])
>>>for person in gedfile.individuals:
... 		print person.source.page
... 		print person.source.data
... 		print person.source.data.text
# Ancestry Family Tree
# Data(2, 'DATA', [Reference(3, 'TEXT', 'http://trees.ancestry.com/pt/AMTCitationRedir.aspx?tid=12345678&pid=21')])
# http://trees.ancestry.com/pt/AMTCitationRedir.aspx?tid=12345678&pid=21
```

##### current available use cases
```
source.value
source.page
source.data
source.data.text
```


## Events

### Residence ['RESI']
Residence records

###### Includes Source class.

```python
>>> for person in gedfile.individuals
...			print person.residence
# Residence(1, 'RESI', 'Marital Status: SingleRelation to Head of House: Son', [Element(2, 'DATE', '1910'), Element(2, 'PLAC', 'Lowell Ward 6, Middlesex, Massachusetts, USA'), Source(2, 'SOUR', '@S1002094821@', [Element(3, 'PAGE', 'Year: 1910; Census Place: Lowell Ward 6, Middlesex, Massachusetts; Roll: T624_600; Page: 33A; Enumeration District: 0864; FHL microfilm: 1374613'), Element(3, '_APID', '1,7884::108099427')])])
>>> for person in gedfile.individuals
...			print person.residence.date
...			print person.residence.source
# 1910
# @S100243564@
```

##### current available use cases
```
residence.date
residence.id
residence.note
residence.parent_id
residence.place
residence.source
residence.value
```

### Events ['EVEN']

Event Records

######Includes the Source class.

```python
>>> for person in gedfile.individuals:
...     print person.happening
# Happening(1, 'EVEN', [Type(2, 'TYPE', 'Arrival'), Date(2, 'DATE', '1901'), Source(2, 'SOUR', '@S10020312532@', [Page(3, 'PAGE', 'Year: 1910; Census Place: Lowell Ward 6, Middlesex, Massachusetts; Roll: T624_600; Page: 33A; Enumeration District: 0864; FHL microfilm: 13764365'), Element(3, '_APID', '1,7884::108024632')])])
>>> for person in gedfile.individuals:
...     print person.happening.type
# Arrival
```

##### current available use cases
```
happening.type      # 'Arrival'
happening.date      # '1901'
happening.place     # 'Lowell Ward 6, Middlesex, Massachusetts'
happening.source    # Source class
```

### Burials ['BURI']
Burials are an extension of the Events class

###### Includes the Source class.

```python
>>> for person in gedfile.individuals:
...     print person.burial
# Burial(1, 'BURI', [Place(2, 'PLAC', "St John's Episcopal Church, Baltimore County, Maryland, USA"), Source(2, 'SOUR', '@S1002127058@', [Element(3, '_APID', '1,60525::5944170')])])
>>> for person in gedfile.individuals:
...     print person.burial.place
# St John's Episcopal Church, Baltimore County, Maryland, USA
```

##### current available use cases

```
burial.place
burial.date
burial.source
```

### Divorce ['DIV']
Divorces are an extension of the Events class

###### Includes the Source class.

```python
>>> for person in gedfile.individuals:
...     print person.divorce
# Divorce(1, 'DIV', [Date(2, 'DATE', 'About 1 Mar 1974'), Place(2, 'PLAC', 'Virginia, USA'), Source(2, 'SOUR', '@S-357317725@', [Note(3, 'NOTE', 'http://trees.ancestry.com/rd?f=sse&db=general-ti=0&indiv=try&gss=pt'), Data(3, 'DATA', [Text(4, 'TEXT', 'divorce date:  About 1 Mar 1974 divorce place:  Virginia, USA birth date:  01 Oct 1941 birth place:  Suffolk, Independent Cities, Virginia, USA Name: Jenny Ann Todd Holladay Todd  marriage date:  1 No', [Element(5, 'CONC', 'v 1962')])]), Element(3, '_APID', '1,9280::1916432')])])
>>> for person in gedfile.individuals:
...     print divorce.date
# About 1 Mar 1974
```

##### current available use cases

```
divorce.place
divorce.date
divorce.source
```

### Error Handling
By default, if a record doesn't exist an error will be raised and will not continue onto the rest of the records. This is on purpose, but can by bypassed by using try/except cases. The most common errors that are raised are IndexError and AttributeError

```python
>>> for person in gedfile.individuals:
...     try:
...         print person.birth.place
...     except AttributeError:
...        print "There is no birth place record for this person"
# There is no birth place record for this person
# Brooklyn, New York City, New York, USA
```
```python
>>> for family in gedfile.families:
...     try:
...         print family.marriage
...     except IndexError as e:
...         print "no record: ", e
# Marriage(1, 'MARR', [Element(2, 'DATE', '08 Aug 1854')])
# no record: IndexError: list index out of range
# Marriage(1, 'MARR', [Element(2, 'DATE', '1954')])
```

### Dates
Dates are user input and can vary wildly in formatting. There are also approximate dates that cannot be formatted. 
These approximate dates can be stripped out using `re` or just `str.replace()`

Using pythons <a href='https://docs.python.org/2/library/datetime.html'>`datetime`</a> library (specifically <a href='https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior'>`strftime`</a> & <a href='https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior'>`strptime`</a>. the dates available can be formatted by looping through various date formats using try/except.

```python
>>> dateFormats = ['%m/%d/%Y', '%m-%d-%Y', '%d-%m-%Y', '%d %b %Y'] #just a few examples
>>> for person in filename.individuals:
...     for i in dateFormat:
...         try:
...             print datetime.strptime(person.birth.date, i)
...         except ValueError: # ValueError will be thrown when the date given does not match the formatting provided from the dateFormat list
...             pass
```
To discover more dates add a counter and increment as it passes through the dateFormat list. If the counter is higher than the length of the list -1 raise an exception printing the date that broke the program.