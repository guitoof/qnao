// import nao api

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

#include <alproxies/alspeechrecognitionproxy.h>
#include <alproxies/almemoryproxy.h>


class RewardModule(ALModule, ALSpeechRecognitionProxy):
	'reward class for NAO'

	# Global variable to store the HumanGreeter module instance
	memory = None
	_reward = 5 ;

	# Constructor 
	def __init__():
		ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")

		# Subscribe to the RearTactilTouched event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("RearTactilTouched",
            "RewardModule",
            "onRearTactilTouched")


        # choose language and words to be recognized during init
		ALSpeechRecognitionProxy::setLanguage('French')
		ALSpeechRecognitionProxy::setVocabulary("pas du tout", true)

		# Subscribe to the WordRecognized event:
		global memory2
        memory2 = ALProxy("ALMemory")
        memory2.subscribeToEvent("WordRecognized",
            "RewardModule",
            "onWordRecognized")




	# methods
	def getReward():
		return _reward 

	def setReward(value):
		_reward = value




	def onRearTactilTouched(self, *_args):
		# Unsubscribe to the event to avoid repetitions
		memory.unsubscribeToEvent("RearTactilTouched",
            "RewardModule")

		self.tts.say("Hello, reward has been updated to one, thank you !")
		self._reward = 1

        # Subscribe again to the event
        memory.subscribeToEvent(("RearTactilTouched",
            "RewardModule",
            "onRearTactilTouched")
        pass


	def onWordRecognized(self, *_args):
		# Unsubscribe to the event to avoid repetitions
		memory2.unsubscribeToEvent("WordRecognized",
            "RewardModule")

		self.tts.say("Hello, reward has been updated to zero, I am so sorry !")
		self._reward = -1
		
		 # Subscribe again to the event
        memory.subscribeToEvent(("WordRecognized",
            "RewardModule",
            "onWordRecognized")		
        pass











