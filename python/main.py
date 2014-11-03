#!/usr/bin python

ip = "169.254.51.192"
NAO_IP = "nao.local"
port = 9559

from naoqi import ALProxy

from armcontroller import ArmController
from reward import Reward

from naoqi import ALBroker
from optparse import OptionParser

import sys
import time


def stand():
    # Posture proxy #
    try:
         postureProxy = ALProxy("ALRobotPosture", ip, 9559)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    postureProxy.goToPosture("Stand", 0.5)

####### Init proxies #######

# Make robot stand if not standing
#stand()

#armController = ArmController(ip, port)
#time.sleep(2)

parser = OptionParser()
parser.add_option( "--pip", help="Parent broker port. The IP Address or your robot", dest="pip" )
parser.add_option( "--pport", help="Parent broker port. The port NAOqi is listening to", dest="pport", type="int" )
parser.set_defaults( pip=ip, pport=port )


(opts, args_) = parser.parse_args()
pip = opts.pip
pport = opts.pport

myBroker = ALBroker( "myBroker",
                     "0.0.0.0", # Listen to anyone
                     0,         # Find a free port and use it
                     pip,
                     pport
                    )


rewardModule = Reward("rewardModule")
goodMemory = ALProxy("ALMemory")
goodMemory.subscribeToEvent( "FrontTactilTouched", "rewardModule", "onFrontTactilTouched" )
badMemory = ALProxy("ALMemory")
badMemory.subscribeToEvent( "RearTactilTouched", "rewardModule", "onRearTactilTouched" )


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print
    print "Interrupted by user. Shutting down ..."
    myBroker.shutdown()
    sys.exit(0)

#armController.move('down')

