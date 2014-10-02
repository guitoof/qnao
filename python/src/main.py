#!/usr/bin python

ip = "169.254.51.192"
port = 9559

from ArmController import ArmController
from naoqi import ALProxy
import time


def stand():
    # Posture proxy #
    try:
         postureProxy = ALProxy("ALRobotPosture", ip, 9559)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    postureProxy.goToPosture("StandInit", 0.5)

####### Init proxies #######

# Make robot stand if not standing
#stand()


armController = ArmController(ip, port)

#time.sleep(2)

#armController.move('left')

