#!/usr/bin python
# -*- coding: utf-8 -*-


__author__ = 'guillaumediallo-mulliez'


import motion
import time
from naoqi import ALProxy

class ArmController:
    """
        This class will control the motion of the robot arm to make it realize the different actions
        Actions are movements of the arm in the following directions :
            * Up : -45° LShoulderPitch
            * Down : +45° LShoulderPitch
            * Left : +20° LShoulderRoll
            * Right : -20° LShoulderRoll
            * Stay
        Arm movement is therefore constraint within the following range :
            * Horizontal range : [-20° +20°]
            * Vertical range : [-45° +45°]
    """

    # Arm states #
    #armState = { 'LShoulderPitch' : 0, 'LShoulderRoll' : 0 }
    armState = {}

    # Movement steps
    step = { 'vertical' : 45, 'horizontal' : 20 }
    # Movement boundaries #
    boundaries = { 'top' : -45, 'bottom' : 45, 'left' : 20, 'right' : -20 }

    # Motion fraction speed
    pFractionMaxSpeed = 0.09


    def __init__(self, robotIp, robotPort):
        try:
            self.motionProxy = ALProxy("ALMotion", robotIp, robotPort)
        except Exception, e:
            print 'Could not create proxy to ALMotion'
            print 'Error was: ', e

        # Init robot arm to center position
        print("Initializing arm to center state ")
        self.resetArmPosition()

    def resetArmState(self):
        self.armState = { 'LShoulderPitch' : 0, 'LShoulderRoll' : 0, 'LElbowYaw' : 0, 'LElbowRoll' : 0 }

    def resetArmPosition(self):
        self.resetArmState()
        armPosition = [ x * motion.TO_RAD for x in self.armState.values()]
        self.motionProxy.angleInterpolationWithSpeed(self.armState.keys(), armPosition, self.pFractionMaxSpeed)

    def move(self, direction):
        #print self.armState['LShoulderPitch'], " and ", self.armState['LShoulderRoll']
        if ( direction == 'up' ):
            self.armState['LShoulderPitch'] = min( self.boundaries['top'], self.armState['LShoulderPitch'] - self.step['vertical'] )
        elif ( direction == 'down' ):
            self.armState['LShoulderPitch'] = max( self.boundaries['bottom'], self.armState['LShoulderPitch'] + self.step['vertical'] )
        elif ( direction == 'left' ):
            self.armState['LShoulderRoll'] = max( self.boundaries['left'], self.armState['LShoulderRoll'] + self.step['horizontal'] )
        elif ( direction == 'right' ):
            self.armState['LShoulderRoll'] = min( self.boundaries['right'], self.armState['LShoulderRoll'] - self.step['horizontal'] )
        armPosition = [ x * motion.TO_RAD for x in self.armState.values()]
        ret = self.motionProxy.angleInterpolationWithSpeed(self.armState.keys(), armPosition, self.pFractionMaxSpeed)
        print ret
        print self.armState['LShoulderPitch'], " and ", self.armState['LShoulderRoll']
        print 'Moving ', direction
