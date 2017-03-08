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
    moving, startTime = False, 0
    dblist, d_thresh = 0, 3
    signals = list()

    for row in iter(p.stdout.readline, b''):
        keypress = drone.getKey()

        # cleanup and exit on keypress
        if keypress:
            # s.close()      # close connection
            drone.land()   # land drone
            exit(0)

        # stop moving if moving for more than 1s
        if moving and time.time() - startTime >= 1.5:
            drone.stop()
            moving = False

        # s.sendall(str(name) + " " + row)
        db_string = re.search("(?<= -).*(?=dB)", row)

        if db_string:
            signals.append(abs(int(db_string.group())))

            # get new (average) signal strength, once enough data points gathered from a tracker
            if len(signals) >= 5:
                new_signal_strength = sum(signals)/len(signals)
                print "RSSI: {0},{1}".format(new_signal_strength, db_string.group())

                # don't influence direction if moving
                # if moving:  pass
                # identify direction of movement of target
                # same position
                if dblist - d_thresh < new_signal_strength < dblist + d_thresh:
                    # drone.moveForward(0.05)
                    # moving = True
                    # startTime = time.time()
                    # print "Probe Forward"
                    pass
                # move towards tracker
                elif new_signal_strength < dblist and not moving:
                    drone.moveBackward(0.05)
                    moving = True
                    startTime = time.time()
                    print "Closer"
                # move away from tracker
                elif not moving:
                    drone.moveForward(0.05)
                    moving = True
                    startTime = time.time()
                    print "Further"

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
