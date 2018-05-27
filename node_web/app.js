var express = require('express');
var app = express();
var child_process = require('child_process'); 
app.get('/', function (req, res) {
  res.send('Hello World node11!');
});

app.get('/frpc', function (req, res) {
    // child_process.exec('/bin/sh /home/pi/pi3-script/node_web/shell/frpc.sh',null,function (err, stdout, stderr) {
    //     console.log('frpc sh ./shell/frpc.sh!',err,stdout.stderr);
    // });
    res.send('frpc success!');
});
var server = app.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;
  console.log('Example app listening at http://%s:%s', host, port);
});