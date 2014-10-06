// import nao api

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

#include <alproxies/alspeechrecognitionproxy.h>
#include <alproxies/almemoryproxy.h>

# to add in main :
ALSpeechRecognitionProxy::setWordListAsVocabulary("words to be recognized")


class RewardModule(ALModule):
	'reward class for NAO'

	# Global variable to store the HumanGreeter module instance
	memory = None
	reward = 5 ;

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
            "Reward",
            "onRearTactilTouched")

		# Subscribe to the WordRecognized event:
        global memory2
        memory2 = ALProxy("ALMemory")
        memory2.subscribeToEvent("WordRecognized",
            "Reward",
            "onWordRecognized")




	# methods
	def getReward():
		return reward 

	def setReward(value):
		reward = value




	def onRearTactilTouched(self, *_args):
		# Unsubscribe to the event to avoid repetitions
		memory.unsubscribeToEvent("RearTactilTouched",
            "Reward")

		self.tts.say("Hello, reward has been updated to one, thank you !")
		reward = 1

        # Subscribe again to the event
        memory.subscribeToEvent(("RearTactilTouched",
            "Reward",
            "onRearTactilTouched")


	def onWordRecognized(self, *_args):
		# Unsubscribe to the event to avoid repetitions
		memory2.unsubscribeToEvent("WordRecognized",
            "Reward")

		self.tts.say("Hello, reward has been updated to zero, I am so sorry !")
		reward = 0
		
		 # Subscribe again to the event
        memory.subscribeToEvent(("WordRecognized",
            "Reward",
            "onWordRecognized")		











