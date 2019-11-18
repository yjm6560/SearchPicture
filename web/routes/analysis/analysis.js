var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var pythonShell = require('python-shell');
var path = require('path');

app.use(bodyParser.urlencoded({extended: false}));

var analysis = {
    show : function(req, res) {
        var scriptPath = path.resolve('..', 'Launcher.py');
        console.log(scriptPath);
        var pythonOptions = {
            mode: 'text',
            pythonPath: '',
            pythonOptions: [],
            scriptPath: '',
            args: []
        };

        pythonShell.PythonShell.run(scriptPath, pythonOptions, function(err, results) {
            if (err) {
                console.error(err);
            }

            console.log('results: %j', results);

            res.render('analysis/analysis', {results:results});
        });
    }
};

module.exports = analysis;