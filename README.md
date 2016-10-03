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
* `python2.7` : see above
* `pip` (package installer python)
* `pytime` : `pip install pytime`
* `gedcompy` : see below
##### Node Modules
* `child-process` - running python from node
* `multer` - for uploading files
* `body-parser`
* `express`
* `mongoose`

### GedcomPy
DO NOT clone from the gedcompy git, I have made changes for this use of gedcompy

navigate into the gedcompy folder and install:

  `cd gedcompy`

  `python setup.py build`
  
  `python setup.py install` - may have to use sudo
  
## Usage (from terminal):
* Move the gedcom file into the GedComParse folder for use.

Usage: `python gedcomparse.py [-h] INPUT_FILE.ged OUTPUT_FILE.json`

> Parse a .gedcom file into .json for use in FamilyGenie

## Usage (from Node server):
```javascript
// multer options
var upload = multer({ dest : 'uploads/' });
// executable child process:
var exec = require('child_process').exec;
//run the process on post
app.post('/uploads', upload, 
    function(req,res,next) {
        exec('python //run python
        path/to/gedcomparse.py //on this program
        path/to/gedcom-file.ged //using this file
        path/to/new-json-file.json', //to this file
        function(err) {
            if(err) { 
                console.log(err); 
            }
            // then to put the files into mongo ...
            exec('mongoimport 
                --db database 
                --collection collection 
                --type json 
                --file path/to/json-file.json 
                --jsonArray', 
                function(err) {
                    if(err) {
                        console.log(err);
                    }
            });
        });
    res.redirect('/');
});

```

