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
    event_received = False

    def __init__(self, _name, broker_name, nao_ip, nao_port):
        self.name = _name
        broker = ALBroker(broker_name,
                     "0.0.0.0", # Listen to anyone
                     0,         # Find a free port and use it
                     nao_ip,
                     nao_port)

        ALModule.__init__(self, _name)
        self.positive_memory = ALProxy("ALMemory")
        self.negative_memory = ALProxy("ALMemory")
        self.success_memory = ALProxy("ALSpeechRecognition")
        wordList=["test","bonjour","Bravo"]
        #self.success_memory.setWordListAsVocabulary( "test", "bravo", "bonjour")

    def subscribe_to_events(self):
        self.positive_memory.subscribeToEvent( "FrontTactilTouched", self.name, "onFrontTactilTouched" )
        self.negative_memory.subscribeToEvent( "RearTactilTouched", self.name, "onRearTactilTouched" )
        self.success_memory.subscribe(self.name)


    def unsubscribe_to_events(self):
        self.positive_memory.unsubscribeToEvent("FrontTactilTouched", self.name)
        self.negative_memory.unsubscribeToEvent("RearTactilTouched", self.name)
        self.success_memory.unsubscribe(self.name)

    def reset(self):
        self.value = 0
        self.event_received = False
        self.unsubscribe_to_events()

    def positiveReward(self):
        self.value = 1
        self.event_received = True

    def negativeReward(self):
        self.value = -1
        self.event_received = True

    def onFrontTactilTouched(self, *_args):
        """
            Callback method for FrontTactilTouched event
        """
        if not(self.event_received):
            self.positiveReward()

    def onRearTactilTouched(self, *_args):
        """
            Callback method for RearTactilTouched event
        """
        if not(self.event_received):
            self.negativeReward()
