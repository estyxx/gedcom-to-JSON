# GedcomParse
Parse JSON data out of a .gedcom file using gedcompy & python2.7

>TODO:
  >>get family relations (currently only gets person data)
  
## Installation:
### Python
<a href="http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/"> Mac Installation </a>

<a href="http://www.howtogeek.com/197947/how-to-install-python-on-windows/"> Windows Installation </a>

<a href="http://docs.python-guide.org/en/latest/starting/install/linux/"> Linux Installation </a>
  
### GedcomParse
##### For Local use:
Clone from this repository & move any .gedcom files into the GedComParse folder to be parsed into json.
##### Requirements
* python2.7
* pip (package installer python)
* pytime: `pip install pytime`
* gedcompy: see below

### GedcomPy
DO NOT clone from the gedcompy git, I have made changes for this use of gedcompy

navigate into the gedcompy folder and install:

  `cd gedcompy`

  `python setup.py build`
  
  `python setup.py install` - may have to use sudo
  
## Usage:
* Move the gedcom file into the GedComParse folder for use.

Usage: `python gedcomparse.py [-h] -i INPUT\_FILE -o OUTPUT\_FILE`

> Parse a .gedcom file into .json for use in FamilyGenie

> optional arguments:

  `-h, --help            show this help message and exit`
  
  `-i INPUT\_FILE, --input INPUT\_FILE`
  
  `-o OUTPUT\_FILE, --output OUTPUT\_FILE`