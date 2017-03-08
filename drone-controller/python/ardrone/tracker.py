#########
# moveTurn.py
# This program is part of the online PS-Drone-API-tutorial on www.playsheep.de/drone.
# It shows how to do complex movements with a Parrot AR.Drone 2.0 using the PS-Drone-API.
# The drone will be flying.
# Dependencies: a POSIX OS, PS-Drone-API 2.0 beta or higher.
# (w)+(c) J. Philipp de Graaff, www.playsheep.de, 2014
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########

##### Suggested clean drone startup sequence #####
import time, sys
import ps_drone                                                  # Import PS-Drone-API

if len(sys.argv) < 2:
    print "Please pass in the IP Address of the drone as a parameter, 192.168.1.1 by default"
    sys.exit(0)

ip = sys.argv[1] if len(sys.argv) > 1 else "192.168.1.1"

drone = ps_drone.Drone()                       # Start using drone
drone.startup(ip)                              # Connects to drone and starts subprocesses

drone.reset()                                                    # Sets drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == -1):   time.sleep(0.1)           # Waits until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])   # Gives the battery-status
if drone.getBattery()[1] == "empty":   sys.exit()                # Give it up if battery is empty
 
drone.useDemoMode(True)                                          # Just give me 15 basic dataset per second (is default anyway)
drone.getNDpackage(["demo"])                                     # Packets, which shall be decoded
time.sleep(0.5)                                                  # Give it some time to awake fully after reset

drone.trim()                                                     # Recalibrate sensors
drone.getSelfRotation(5)                                         # Getting value for auto-alteration of gyroscope-sensor
print "Auto-alternation: "+ str(drone.selfRotation)+" dec/sec"    # Showing value for auto-alteration

drone.takeoff()                                                  # Fly, drone, fly !
while drone.NavData["demo"][0][2]:     time.sleep(0.1)           # Wait until the drone is really flying (not in landed-mode anymore)

##### Mainprogram begin #####
print "Drone is flying now"

time.sleep(5)

print "Drone moves forward"
leftRight       = 0.0                                        # Move with 2% speed to the left
backwardForward = 0.05                                           # Move with 10% speed backwards
downUp          = 0.0                                            # Move with 30% speed upward
turnLeftRight   = 0.0                                              # Turn full speed right
drone.move(leftRight, backwardForward, downUp, turnLeftRight)    # Do movement

timeToFlight    = 5.0                                            # Time to fly at all 
refTime         = time.time()                                    # Start-time
end             = False
while not end:
    if drone.getKey():                        sys.exit()         # Stop when any key is pressed
    if time.time()-refTime >= timeToFlight:   end = True         # Stop when max time of flight has been reached

drone.stop()
time.sleep(5)

print "now Drone moves backward"

backwardForward = -backwardForward
drone.move(leftRight, backwardForward, downUp, turnLeftRight)    # Do movement
timeToFlight    = 5.0                                            # Time to fly at all 
refTime         = time.time()                                    # Start-time
end             = False
while not end:
    if drone.getKey():                        sys.exit()         # Stop when any key is pressed
    if time.time()-refTime >= timeToFlight:   end = True         # Stop when max time of flight has been reached

print "Drone stopped movement"
drone.stop()
time.sleep(2)
drone.land()
