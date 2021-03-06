#########
# firstTagDetection.py
# This program is part of the online PS-Drone-API-tutorial on www.playsheep.de/drone.
# It shows how to detect tag/marker of a Parrot AR.Drone 2.0 using the PS-Drone-API.
# Dependencies: a POSIX OS, PS-Drone-API 2.0 beta or higher.
# (w) J. Philipp de Graaff, www.playsheep.de, 2014
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########

##### Suggested clean drone startup sequence #####
import time, sys
import ps_drone                                                # Import PS-Drone

if len(sys.argv) < 2:
    print "Please pass in the IP Address of the drone as a parameter, 192.168.1.1 by default"
    sys.exit(0)

ip = sys.argv[1] if len(sys.argv) > 1 else "192.168.1.1"

drone = ps_drone.Drone()                       # Start using drone
drone.startup(ip)                              # Connects to drone and starts subprocesses

print "droneIP: " + drone.DroneIP

drone.reset()                                                  # Sets the drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == - 1):   time.sleep(0.1)        # Wait until the drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])    # Gives a battery-status
if drone.getBattery()[1] == "empty":   sys.exit()                # Give it up if battery is empty

drone.useDemoMode(False)                                        # Just give me 15 basic dataset per second (is default anyway)
drone.getNDpackage(["demo", "vision_detect"])                   # Packets, which shall be decoded
time.sleep(0.5)                                                # Give it some time to awake fully after reset

# drone setup
drone.trim()                                                     # Recalibrate sensors
drone.getSelfRotation(5)                                         # Getting value for auto-alteration of gyroscope-sensor
print "Auto-alternation: "+str(drone.selfRotation)+" dec/sec"    # Showing value for auto-alteration

drone.takeoff()                                                  # Fly, drone, fly !
while drone.NavData["demo"][0][2]:     time.sleep(0.1)           # Wait until the drone is really flying

drone_iniz, drone_inix, drone_iniy = 0, 0, 0

##### Mainprogram begin #####
# Setting up detection...
# Shell-Tag=1, Roundel=2, Black Roundel=4, Stripe=8, Cap=16, Shell-Tag V2=32, Tower Side=64, Oriented Roundel=128
drone.setConfig("detect:detect_type", "3")                     # Enable universal detection
drone.setConfig("detect:detections_select_h", "0")           # Detect "Oriented Roundel" with front-camera
drone.setConfig("detect:detections_select_v", "128")             # No detection with ground cam
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:    time.sleep(0.01)        # Wait until configuration has been set

drone.setConfig("control:flying_mode", "2")                   # auto stabilization of drone distance from marker

# Get detections
stop = False
moving = False
reversing = False
found = False

moves = [((0, 0.08, 0, 0), 1), ((0, -0.08, 0, 0), 1), ((0.08, 0, 0, 0), 1), ((-0.08, 0, 0, 0), 1), ((0.08, 0.08, 0, 0), 1), ((-0.08, -0.08, 0, 0), 1), ((0.08, -0.08, 0, 0), 1), ((-0.08, 0.08, 0, 0), 1), ]
moveNum = 0
startTime = 0

baseX = 250
baseY = 150

timeStable = 0
stableStart = 0
stable = False


while not stop:
    NDC = drone.NavDataCount
    while NDC == drone.NavDataCount:   time.sleep(0.01)

    keyPress = drone.getKey();

    if keyPress:
        if keyPress != 'w' and keyPress != 's':   
            print keyPress             
            stop = True
        elif keyPress == 'w':
            drone.moveUp(0.4)
            time.sleep(0.2)
            drone.stop();
        elif keyPress == 's':
            drone.moveDown(0.4)
            time.sleep(0.2)
            drone.stop();

    # Loop ends when key was pressed
    tagNum = drone.NavData["vision_detect"][0]                 # Number of found tags
    tagX =   drone.NavData["vision_detect"][2]                 # Horizontal position(s)
    tagY =   drone.NavData["vision_detect"][3]                 # Vertical position(s)
    tagZ =   drone.NavData["vision_detect"][6]                 # Distance(s)
    tagRot = drone.NavData["vision_detect"][7]                 # Orientation(s)

    ###Drone stabilization
    if tagNum:

        #print "Tag Found"

        #found = True

        if moving:
            print "Stopping Previous move"
            drone.stop()
            moving = False

        if not drone_iniz:
            drone_inix, drone_iniy, drone_iniz = tagX[0], tagY[0], tagZ[0]
            print "Initial X, Y, Z:", drone_inix, drone_iniy, drone_iniz
            drone.hover()
            time.sleep(1)
        

        # if tagZ[0] <= drone_iniz:
        #     drone.moveUp(0.2)
        #     #print "Moving Up"
        # elif tagZ[0] > drone_iniz+10:
        #     drone.moveDown(0.2)
        #     #print "\t\tMoving Down"
        # elif drone_iniz < tagZ[0] < drone_iniz+10:
        #     drone.stop()
        #     time.sleep(0.2)
        #     drone.hover()
        #     #print "\t\t\t\tNo Movement"
        
        if  stable == False:
            if tagX[0] < baseX - 50:
                stableStart = 0
                timeStable = 0
                drone.moveRight(0.05)
            elif tagX[0] > baseX + 50:
                stableStart = 0
                timeStable = 0
                drone.moveLeft(0.05);
            else:
                drone.stop()
                time.sleep(0.2)

                if stableStart == 0:
                    stableStart = time.time()
                else:
                    timeStable = time.time() - stableStart

                    if timeStable >= 2:
                        stable = True

                #drone.hover()

            if tagY[0] < baseY - 50:
                stableStart = 0
                timeStable = 0
                drone.moveForward(0.05)
            elif tagY[0] > baseY + 50:
                stableStart = 0
                timeStable = 0
                drone.moveBackward(0.05);
            else:
                drone.stop()
                time.sleep(0.2)

                if stableStart == 0:
                    stableStart = time.time()
                else:
                    timeStable = time.time() - stableStart

                    if timeStable >= 2:
                        stable = True
                #drone.hover()
        
            for i in range (0,tagNum):
                 print "Tag no "+str(i)+" : X= "+str(tagX[i])+"  Y= "+str(tagY[i])+"  Dist= "+str(tagZ[i])+"  Orientation= "+str(tagRot[i])
        else:
            print "I'm Stable!"

            drone.moveUp(0.4)
            time.sleep(1)
            drone.stop()
            stable = False
    else:
        moving = False
        # if found == False:
        #     currMove = moves[moveNum]

        #     if moving == False:
        #         drone.move(currMove[0][0], currMove[0][1], currMove[0][2], currMove[0][3])
        #         #drone.turnRight(0.5)
        #         moving = True
        #         startTime = time.time()
        #     else:
        #         if (time.time() - startTime >= currMove[1]):
        #             if reversing == False:
        #                 drone.stop();
        #                 time.sleep(0.2)

        #                 drone.move(-currMove[0][0], -currMove[0][1], -currMove[0][2], -currMove[0][3])
        #                 reversing = True
        #                 startTime = time.time();
        #             else:
        #                 drone.stop();
        #                 time.sleep(0.2)

        #                 moving = False
        #                 reversing = False
        #                 moveNum = moveNum + 1

        #                 if (moveNum >= len(moves)):
        #                     moveNum = 0;


        #print "\t\t\t\t\t\tNo tag detected (" + str(moveNum) + ")"

drone.land()
