var express = require('express');
var app = express();
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();
var bodyParser = require('body-parser');
var path = require('path');

app.use(bodyParser.urlencoded({extended: false}));

var db_path = path.resolve(path.join('..','photo_data_admin.db'));
let db = new sqlite3.Database(db_path, sqlite3.OPEN_READWRITE, (err) => {
    console.log(db_path);
    if (err) {
        console.error(err.message);
    } else {
        console.log('Connected to the photo_data_admin database.');
    }
});

var searchResult = {
    show : function(req, res) {
        var keywords = req.body.keywords;
        var keyword_list = keywords.split(',');

        var option = req.body.option;

        var object_query = '';
        var text_query = '';

        //FROM에 테이블 이름
        var table_name = 'photo_data_easy';

        //태그 검색 : WHERE tag_list LIKE "%/dog/%"
        //텍스트 검색 : WHERE text_img LIKE "%dog%"
        var k;
        var i;
        if (option == 'ot') {
            //object + text search
            k = 'tag_list LIKE \"%/' + keyword_list[0] + '/%\"';
            i = 1;
            while( i < keyword_list.length ) {
                k = k + ' AND tag_list LIKE \"%/' + keyword_list[i].trim() + '/%\"';
                i = i + 1;
            }
            k = k + ';';

            object_query = `SELECT path FROM ${table_name} WHERE ${k}`;

            k = 'text_img LIKE \"%' + keyword_list[0] + '%\"';
            i = 1;
            while( i < keyword_list.length ) {
                k = k + ' AND text_img LIKE \"%' + keyword_list[i].trim() + '%\"';
                i = i + 1;
            }
            k = k + ';';

            text_query = `SELECT path FROM ${table_name} WHERE ${k}`;
        } else if (option == 'o') {
            //object search
            k = 'tag_list LIKE \"%/' + keyword_list[0] + '/%\"';
            i = 1;
            while( i < keyword_list.length ) {
                k = k + ' AND tag_list LIKE \"%/' + keyword_list[i].trim() + '/%\"';
                i = i + 1;
            }
            k = k + ';';

            object_query = `SELECT path FROM ${table_name} WHERE ${k}`;
        } else if (option == 't') {
            //text search
            var k = 'text_img LIKE \"%' + keyword_list[0] + '%\"';
            var i = 1;
            while( i < keyword_list.length ) {
                k = k + ' AND text_img LIKE \"%' + keyword_list[i].trim() + '%\"';
                i = i + 1;
            }
            k = k + ';';

            text_query = `SELECT path FROM ${table_name} WHERE ${k}`;
        }

        var object_row = [];
        var text_row = [];
        if (object_query != '') {
            db.serialize(( ) => {
                db.all(object_query, (err, row) => {
                    if (err) {
                        console.error(err.message);
                    }
                    console.log('row');
                    console.log(row);
                    object_row = row.slice();
                    console.log('object_row');
                    console.log(object_row);
                });
            });
        }
        if (text_query != '') {
            db.serialize(( ) => {
                db.all(text_query, (err, row) => {
                    if (err) {
                        console.error(err.message);
                    }
                    //console.log(row);
                    text_row = row.slice();
                });
            });
        }

        console.log(object_row);
        console.log(text_row);

        res.render('search/searchResult', {option:option, object_row:object_row, text_row:text_row});
    }
};

module.exports = searchResult;