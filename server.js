var express = require('express');
var multer = require('multer');
var bodyParser = require('body-parser');
var spawn = require('child_process').spawn;
// var mongoose = require('mongoose');

// upload things
var upload = multer({ storage: multer.memoryStorage({}) });
var type = upload.single('sampleFile'); // sampleFile must match name of input on frontend

var app = express();
var PORT = 8000;

// mongo connection
// mongoose.connect('mongodb://localhost');
// var db = mongoose.connection;
// var people = require('./people.model')(mongoose); // change this to your people model

// get the info from the upload button
app.post('/uploads', type, function(req, res, next) {
  var contents = req.file.buffer.toString(); //get the contents from the upload as a string
  res.redirect('/');
  var process = spawn('python',['./gedcomparse.py', contents]); // run the python program on the info
  process.stdout.on('data', function(data) {
    // console.log(data.toString());
    jsonInfo = JSON.parse(JSON.stringify(data.toString())); // parse the data into json
    // console.log(jsonInfo);
    // people.insertMany(jsonInfo);
  });
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
