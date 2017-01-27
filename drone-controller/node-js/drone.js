var arDrone = require('ar-drone');
var client  = arDrone.createClient();

client.takeoff();

var time = 2000;

client
   .after(1000, function(){
  	this.calibrate(0);
  }).after(3000, function(){
  	this.stop();
    this.right(0.10);
  }).after(time, function() {
  	this.stop();
  	this.back(0.10);
  }).after(time, function() {
  	this.stop();
  	this.left(0.10);
  }).after(time, function() {
  	this.stop();
  	this.front(0.10);
  }).after(time, function() {
  	this.stop();
  	//client.animate('flipLeft', 1000);
  	this.land();
  });