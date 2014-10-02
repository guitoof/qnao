#!/usr/bin python

__author__ = 'guillaumediallo-mulliez'


import motion
import time
from naoqi import ALProxy

class ArmController:
    """This class will control the motion of the robot arm to make it realize the different actions"""
    # Motion proxy #
    #ALProxy motionProxy

    # Joint names #
    jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]

    # Arm states #
    armState = [0,  25, 0, -30]

    # Motion fraction speed
    pFractionMaxSpeed = 0.3


    def __init__(self, robotIp, robotPort):
        try:
            self.motionProxy = ALProxy("ALMotion", robotIp, robotPort)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e

        # Init robot arm to center position
        #print("Initializing arm to center state ")
        newArmState = [ x * motion.TO_RAD for x in self.armState]
        #self.motionProxy.angleInterpolationWithSpeed(self.jointNames, self.armState, self.pFractionMaxSpeed)


    def do(self, action):
        newArmState = self.armState
        if ( action == "up" ):
            newArmState[0] += 45
        elif ( action == "down" ):
            newArmState[0] -= 45
        elif ( action == "left" ):
            newArmState[1] += 10
        elif ( action == "right" ):
            newArmState[1] -= 10
        if (newArmState[0] >= -45 and newArmState[0] <= 45 and newArmState[1] >= 10 and newArmState[1] <= 40 ):
            newArmState = [ x * motion.TO_RAD for x in newArmState]
            print("Arm is moving ", action)
            self.motionProxy.angleInterpolationWithSpeed(self.jointNames, newArmState, self.pFractionMaxSpeed)
        time.sleep(1.0)

