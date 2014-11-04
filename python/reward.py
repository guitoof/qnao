#!/usr/bin python
# -*- coding: utf-8 -*-

import sys
import time

from naoqi import ALProxy
from naoqi import ALModule


class Reward(ALModule):

    value = 0
    event_received = False

    def __init__(self, _name):
        self.name = _name
        ALModule.__init__(self, _name)
        self.memory = ALProxy("ALMemory")
        self.speechRecognizer = ALProxy("ALSpeechRecognition")
        for subscriber in self.speechRecognizer.getSubscribersInfo():
            self.speechRecognizer.unsubscribe(subscriber[0])
        vocabulary=["bravo"]
        self.speechRecognizer.setVocabulary(vocabulary, False)

    def subscribe_to_events(self):
        self.memory.subscribeToEvent( "FrontTactilTouched", self.name, "onFrontTactilTouched" )
        self.memory.subscribeToEvent( "RearTactilTouched", self.name, "onRearTactilTouched" )
        self.speechRecognizer.subscribe("success_event")


    def unsubscribe_to_events(self):
        self.memory.unsubscribeToEvent("FrontTactilTouched", self.name)
        self.memory.unsubscribeToEvent("RearTactilTouched", self.name)
        self.speechRecognizer.unsubscribe("success_event")

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

    def successReward(self):
        self.value = 10
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
