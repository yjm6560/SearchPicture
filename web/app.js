//필요한 모듈 선언
var express = require('express');
var http = require('http');
var app = express();

//express 서버 포트 설정(8080)
app.set('port', process.env.PORT || 8080);

//서버 생성
http.createServer(app).listen(app.get('port'), function(){
    console.log('Express server listening on port ' + app.get('port'));
});

//라우팅 모듈 선언
var indexRouter = require('./routes/index');

//request 요청 URL과 처리 로직을 선언한 라우팅 모듈 매핑
app.use('/', indexRouter)