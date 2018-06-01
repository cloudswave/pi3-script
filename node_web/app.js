"use strict"
var express = require('express');
var app = express();
var child_process = require('child_process');
var spawnObj = null;
var current_status = "stop";
app.get('/', function(req, res) {
    res.send('Hello World node11!');
});
app.get('/music/:status/:url', function(req, res) {
    res.send('music: ' + req.params.status + ':' + req.params.url);
    let status = req.params.status;
    let url = decodeURIComponent(req.params.url);
    if (!spawnObj) {
        spawnObj = child_process.spawn('mpg123', ['-R'], {
            encoding: 'utf-8'
        });
        spawnObj.stdout.on('data', function(chunk) {
            console.log(chunk.toString());
        });
        spawnObj.stderr.on('data', (data) => {
            console.log(data);
        });
        spawnObj.on('close', function(code) {
            console.log('close code : ' + code);
        });
        spawnObj.on('exit', (code) => {
            console.log('exit code : ' + code);
        });
        spawnObj.stdin.write('V 60\n');
    }
    try {
        
        switch (status) {
            case 'play':
                    spawnObj.stdin.write(`L ${url}\n`);
                break;
            case 'stop':
                if(spawnObj) {
                    spawnObj.stdin.write('Q\n');
                    spawnObj.kill();
                    spawnObj = null;                    
                }

                break;
            case 'pause':
                if(spawnObj) {
                    spawnObj.stdin.write('P\n');
                }
                break;
            case 'resume':
                if(spawnObj)
                    spawnObj.stdin.write('P\n');
            default:
                // code
        }
        current_status = status;
    } catch (e) {
        console.error('error:',e);
    }

});
app.get('/frpc', function(req, res) {
    // child_process.exec('/bin/sh /home/pi/pi3-script/node_web/shell/frpc.sh',null,function (err, stdout, stderr) {
    //     console.log('frpc sh ./shell/frpc.sh!',err,stdout.stderr);
    // });
    res.send('frpc success!');
});
var server = app.listen(3000, function() {
    var host = server.address().address;
    var port = server.address().port;
    console.log('Example app listening at http://%s:%s', host, port);
});