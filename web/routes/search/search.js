var express = require('express');
var router = express.Router();

let db = new sqlite3.Database('../photo_data_admin.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.error(err.message);
    } else {
        console.log('Connected to the photo_data_admin database.');
    }
});

router.get('/search', function(request, response){
    res.render('insert');
});

router.post('/', function(req,res,next){
    var keywords = req.body;
    var k = 'text_img LIKE \"%' + keywords[0] + '%\"';
    var i = 0;
    for(i < keywords.length) {
        k = k + ' AND text_img LIKE \"%' + keywords[i] + '%\"';
    }

    const query = `SELECT phto_id, path, tag_list FROM photo_data_admin.db WHERE '${k}'`;

    db.serialize();
    db.all(query, (err, row) => {
        res.render('show', {data:row});
    });
})

