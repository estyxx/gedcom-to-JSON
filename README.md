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

My fork of gedcompy <a href='https://github.com/KingEdwardI/gedcom-to-JSON'> here</a>.