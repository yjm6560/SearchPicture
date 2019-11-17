var express = require('express');
var app = express();
var bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({extended: false}));

var analysisResult = {
    show : function(req, res) {
        res.render('analysis/analysisResult');
    }
};

module.exports = analysisResult;