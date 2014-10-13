#!/usr/bin python
# -*- coding: utf-8 -*-

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

# Global variable to store the HumanGreeter module instance
memory = None

class Reward:
	"""
	    Reward class for NAO
	"""