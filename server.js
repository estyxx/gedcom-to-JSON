var express = require('express');
var multer = require('multer');
var bodyParser = require('body-parser');
var exec = require('child_process').exec;
var mongoose = require('mongoose');

// upload things
var upload = multer({ dest: 'uploads/' });
var type = upload.single('sampleFile'); // sampleFile must match name of input on frontend

var app = express();
var PORT = 8000;

// mongo connection
mongoose.connect('mongodb://localhost');
var db = mongoose.connection;
// var people = require('./people.model')(mongoose); // change this to your people model

// get the info from the upload button
app.post('/uploads', type, function(req, res, next) {

  exec('python ./gedcomparse.py uploads/' + req.file.filename + ' jsonfiles/' + req.file.filename + '.json',  // run the python program on the info
    function(err) {
    if(err) {
      console.log('python parse failed', err);
    }
    else {
      console.log('gedcom saved and parsed to json with python');
    }
  exec('python ./gedcomparent.py uploads/' + req.file.filename + ' jsonfiles/' + req.file.filename + '.json',  // run the python program on the info
    function(err) {
    if(err) {
      console.log('python parse failed', err);
    }
    else {
      console.log('gedcom saved and parsed to json with python');
    }
  exec('python ./gedcompairbonds.py uploads/' + req.file.filename + ' jsonfiles/' + req.file.filename + '.json',  // run the python program on the info
    function(err) {
    if(err) {
      console.log('python parse failed', err);
    }
    else {
      console.log('gedcom saved and parsed to json with python');
    }
  exec('python ./gedcominfo.py uploads/' + req.file.filename + ' jsonfiles/' + req.file.filename + '.json',  // run the python program on the info
    function(err) {
    if(err) {
      console.log('python parse failed', err);
    }
    else {
      console.log('gedcom saved and parsed to json with python');
    }

    exec('mongoimport --db test --collection gedcom_import --type json --file jsonfiles/' + req.file.filename + '.json --jsonArray', function(err) { // imports the file that was just uploaded into mongoDB
      if(err) {
        console.log('mongo import failed', err);
      }
      else {
        console.log('json file imported to mongo');
      }
    });
  });

  res.redirect('/');
});

app.use(function(req, res, next) {
    console.log(req.url);
    next();
});

app.use(express.static(__dirname));

app.get("/", function(req, res) {
    res.sendFile("/index.html");
});

app.listen(PORT, function() {
  console.log('listening on port: ' + PORT);
});
