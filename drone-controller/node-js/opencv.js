var arDrone = require('ar-drone');
var client  = arDrone.createClient();
var http = require('http');
var cv = require('opencv');
var fs = require('fs');


var png = null;

var opts = opts || {};

var server = http.createServer(function(req, res) {

  if (!png) {
    png = client.getPngStream();
    png.on('error', function (err) {
        console.error('png stream ERROR: ' + err);
    });
  }

  res.writeHead(200, { 'Content-Type': 'multipart/x-mixed-replace; boundary=--daboundary' });

  png.on('data', sendPng);

// example face classifier
  function sendPng(buffer) {
    cv.readImage(buffer, function(err, im){
      if (err) throw err;
      if (im.width() < 1 || im.height() < 1) throw new Error('Image has no size');

      im.detectObject("haarcascade_frontalface_alt.xml", {}, function(err, faces){
        if (err) throw err;

        for (var i = 0; i < faces.length; i++){
          var face = faces[i];
          im.ellipse(face.x + face.width / 2, face.y + face.height / 2, face.width / 2, face.height / 2);
        }

        im.save('./tmp/face-detection.png');

        fs.readFile('./tmp/face-detection.png', function(err, data) {

          res.write('--daboundary\nContent-Type: image/png\nContent-length: ' + data.length + '\n\n');
          res.write(data);
        });

      });
    });

  }
});

server.listen(opts.port || 8000);
