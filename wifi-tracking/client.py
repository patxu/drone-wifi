import fileinput
import socket
import sys
import subprocess as sub
import ps_drone                                                # Import PS-Drone
import re
import time

if __name__ == "__main__":

    ip = sys.argv[5]                               # get ip of drone passed by user
    drone = ps_drone.Drone()                       # Start using drone
    drone.startup(ip)                              # Connects to drone and starts subprocesses
    drone.reset()                                  # Sets the drone's status to good (LEDs turn green when red)

    while (drone.getBattery()[0] == - 1):   time.sleep(0.1)        # Wait until the drone has done its reset
    print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])    # Gives a battery-status
    if drone.getBattery()[1] == "empty":   sys.exit()                # Give it up if battery is empty

    drone.trim()                              # Recalibrate sensors
    drone.takeoff()                           # Fly, drone, fly !

    # # connect client to server
    # host = sys.argv[1]
    # port = int(sys.argv[2])                   # The same port as used by the server
    # name = int(sys.argv[3])
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((host, port))

    macs = {'vp': '4c:66:41:3f:61:7a', 'ap': 'ec:1f:72:34:97:2b', 'dp': 'f4:f5:23:3c:8e:08'}
    mac = macs[sys.argv[4]]

    print "Hello :)"
    args = ['sudo', 'tcpdump', '-s', '0', '-tttt', '-vvvv', '-l', '-i', 'mon0', 'ether', 'src', mac]
    p = sub.Popen(args, stdout=sub.PIPE)

    # witrack variable
    moving = True
    first = True
    startTime = time.time()
    dblist, d_thresh = 0, 3
    signals = list()
    moveTime = 5
    numFurther = 0
    direction = 'forward'
    speed = 0.1

    for row in iter(p.stdout.readline, b''):
        keypress = drone.getKey()

        # cleanup and exit on keypress
        if keypress:
            # s.close()      # close connection
            drone.land()   # land drone
            exit(0)

        # stop moving if moving for more than 1s
        if moving and time.time() - startTime >= moveTime:
            drone.stop()
            moving = False
            signals = []

        # s.sendall(str(name) + " " + row)
        db_string = re.search("(?<= -).*(?=dB)", row)

        if db_string:
            signals.append(abs(int(db_string.group())))

            # get new (average) signal strength, once enough data points gathered from a tracker
            if len(signals) >= 5:
                new_signal_strength = sum(signals)/len(signals)
                print "RSSI: {0},{1}".format(new_signal_strength, db_string.group())

                if new_signal_strength > 30 and first:
                    if direction == 'forward':
                        drone.moveForward(speed)
                    else:
                        drone.moveBackward(speed)

                    moving, first = True, False
                    startTime = time.time()
                    moveTime = 1
                    numFurther = 0
                    print "First Motion, Move {0}".format(direction)

                # identify direction of movement of target
                # same position
                if dblist - d_thresh < new_signal_strength < dblist + d_thresh:
                    # drone.moveForward(speed)
                    # print "Probe Forward"
                    # moving = True
                    # startTime = time.time()
                    # moveTime = 2
                    pass
                # move towards tracker
                elif new_signal_strength < dblist and not moving:
                    if direction == 'forward':
                        drone.moveForward(speed)
                    else:
                        drone.moveBackward(speed)

                    moving = True
                    startTime = time.time()
                    moveTime = 1
                    numFurther = 0
                    print "Closer, Move {0}".format(direction)

                # move away from tracker
                elif not moving:
                    if direction == 'forward':
                        drone.moveForward(speed)
                    else:
                        drone.moveBackward(speed)

                    moving = True
                    startTime = time.time()
                    moveTime = 1
                    numFurther = numFurther + 1

                    if numFurther >= 2:
                        numFurther = 0
                        if direction == 'forward':
                            direction = 'backward'
                        else:
                            direction = 'forward'
                    print "Further, Move {0}".format(direction)

                dblist = new_signal_strength
                signal_strength = new_signal_strength
                signals = []  # reset signals from tracker

    # # read data stream from stdin and push to client over tcp4 socket
    # for line in fileinput.input():
    #     s.sendall("1 " + line)
    #     print line

    # cleanup before exit
    # s.close()      # close connection
    # print('Received', repr(data))
    drone.land()   # land drone
    exit(0)
