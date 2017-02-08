var arDrone = require('ar-drone');
var client  = arDrone.createClient();
var http = require('http');
var cv = require('opencv');

// consts for detect shapes
var lowThresh = 0;
var highThresh = 100;
var nIters = 2;
var minArea = 8000;
var maxArea = 25000;
var BLUE  = [0, 255, 0]; // B, G, R
var RED   = [0, 0, 255]; // B, G, R
var GREEN = [0, 255, 0]; // B, G, R
var WHITE = [255, 255, 255]; // B, G, R

client.config('video:video_channel', 3);


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

      var out = new cv.Matrix(im.height(), im.width());
      var im_canny = im.copy();
      im_canny.convertGrayscale();
      im_canny.canny(lowThresh, highThresh);
      im_canny.dilate(nIters);

      contours = im_canny.findContours();

      for (i = 0; i < contours.size(); i++) {

        if (contours.area(i) < minArea) continue;
        if (contours.area(i) > maxArea) continue;

        var arcLength = contours.arcLength(i, true);
        contours.approxPolyDP(i, 0.1 * arcLength, true);

        switch(contours.cornerCount(i)) {
          // case 3:
          //   out.drawContour(contours, i, GREEN);
          //   break;
          case 4:
            out.drawContour(contours, i, RED);
            break;
          // default:
            // out.drawContour(contours, i, WHITE);
        }
      }

      var image = out.toBuffer();
      // var image = im.toBuffer();
      res.write('--daboundary\nContent-Type: image/png\nContent-length: ' + image.length + '\n\n');
      res.write(image);
    });

  }
});

server.listen(opts.port || 8000);
