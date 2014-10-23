#!/usr/bin python
# -*- coding: utf-8 -*-

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

# Global variable to store the HumanGreeter module instance
# memory = None


class Reward(ALModule):

    value = 0

    def positiveReward(self):
        print "Receiving congratulation (+1 reward)"
        self.value += 1

    def negativeReward(self):
        print "Receiving punishment (-1 reward)"
        self.value -= 1

    def onFrontTactilTouched(self, *_args):
        """
            Callback method for FrontTactilTouched event
        """

        self.positiveReward()
        print "Total reward is ", self.value
        pass

    def onRearTactilTouched(self, *_args):
        """
            Callback method for RearTactilTouched event
        """

        self.negativeReward()
        print "Total reward is ", self.value
        pass
