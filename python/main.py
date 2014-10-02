#!/usr/bin python

ip = "169.254.51.192"
port = 9559

import arm_controller
from naoqi import ALProxy

####### Init proxies #######

# Make robot stand if not standing
#stand()


armController = arm_controller.ArmController(ip, port)
armController.do("left")

def stand(self):
    # Posture proxy #
    try:
         postureProxy = ALProxy("ALRobotPosture", ip, 9559)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    postureProxy.goToPosture("StandInit", 0.5)