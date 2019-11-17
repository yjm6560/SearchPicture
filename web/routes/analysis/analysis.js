var express = require('express');
var app = express();
var bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({extended: false}));

var analysis = {
    show : function(req, res) {
        res.render('analysis/analysis');
    }
};

module.exports = analysis;