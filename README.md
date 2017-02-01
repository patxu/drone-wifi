# drone-wifi

## Architecture
[Node.js Drone Package](https://github.com/felixge/node-ar-drone)

## Setup
The **Drone Controller** files can be found in `drone-controller`.

- ### Node.js
  The Node.js controller is found at `node-js`.
  - `npm install`

- ### ROS ARDrone Autonomy
  - primarily followed [this guide](http://wiki.ros.org/tum_ardrone)
  - installed ROS on MacOS via [Docker](http://wiki.ros.org/docker/Tutorials/Docker)
  - also had to follow the [pre-install instructions](https://github.com/tum-vision/ardrone_autonomy#pre-requirements) on the ARDrone Autonomy Github
  - [Docker Hub repo](https://hub.docker.com/r/patxu/ardrone/)

  - connect to two Wifi networks by using a [Wifi card](https://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=sr_1_fkmr0_1?ie=UTF8&qid=1485920981&sr=8-1-fkmr0&keywords=edimax+eq+7811). this will allow you to connect to the drone while maintaining internet service

## The Team
- Asad Alavi, GR
- Debanjum Solanky, GR
- Pat Xu, '17
- Vishal Gaurav, GR
