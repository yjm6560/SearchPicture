var express = require('express');
var app = express();
var router = express.Router();
var sqlite3 = require('sqlite3');
var bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({extended: false}));

let db = new sqlite3.Database('../photo_data_admin.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.error(err.message);
    } else {
        console.log('Connected to the photo_data_admin database.');
    }
});

var search = {
    show : function(req, res) {
        res.render('search/search');
    }
};

var searchResult = require('./searchResult');

/*router.get('/search/result', (req, res) => {
    console.log(req);
    var keywords = req.body.keywords;
    res.send(`keywords : ${keywords}`);
    searchResult.show(req, res);
});*/

module.exports = search;