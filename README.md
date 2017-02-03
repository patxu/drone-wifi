# drone-wifi

## Architecture
[Node.js Drone Package](https://github.com/felixge/node-ar-drone)

to get drone PNG feed install this module using "npm install ar-drone-png-stream"

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
    - check current docker images with `docker images`
      ```
      REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
      patxu/ardrone       latest              550afefe761a        9 hours ago         1.3 GB
      ```
    - run the image with `docker exec -it patxu/ardrone`
    - custom setup script that runs some basic commands at `ardrone_setup.sh`

  - connect to two Wifi networks by using a [Wifi card](https://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=sr_1_fkmr0_1?ie=UTF8&qid=1485920981&sr=8-1-fkmr0&keywords=edimax+eq+7811). this will allow you to connect to the drone while maintaining internet service


## The Team
- Asad Alavi, GR
- Debanjum Solanky, GR
- Pat Xu, '17
- Vishal Gaurav, GR
