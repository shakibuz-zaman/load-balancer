var http = require('http'); // 1 - Import Node.js core module

var server = http.createServer(function (req, res) {   // 2 - creating server

    console.log('Incoming call-------');
    res.writeHead(200);
    res.end("My first server!");
});

server.listen(5011); //3 - listen for any incoming requests

console.log('Node.js web server at port 5000 is running...')