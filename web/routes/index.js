var express = require('express');
var router = express.Router();

var search = require('./search/search');
var searchResult = require('./search/searchResult');
var analysis = require('./analysis/analysis');
var analysisResult = require('./analysis/analysisResult');

//라우터의 get()함수를 이용해 request URL('/')에 대한 업무처리 로직 정의
router.get('/', function(req, res, next){
    res.send('index page');
});

router.get('/search', function(req, res, next){
    search.show(req,res);
    // res.render("search", {page:"search/search"});
});

router.post('/search/result', function(req, res, next) {
    searchResult.show(req, res);
});

router.get('/analysis', function(req, res, next) {
    analysis.show(req, res);
});

router.get('/analysis/result', function(req, res, next) {
    analysisResult.show(req, res);
});

//모듈에 등록해야 app.js에서 app.use 함수를 통해서 사용 가능
module.exports = router;