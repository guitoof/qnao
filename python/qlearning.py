# -*- encoding: UTF-8 -*-

from state import State
import numpy as np
import random
import time
from policies import Policies
from armcontroller import ArmController
from naoqi import ALProxy
from reward import Reward
from naoqi import ALBroker

reward_module = Reward("reward_module", "nao_broker", "169.254.51.192", 9559)


class QLearning(object):
    "QLearning main class"

    def __init__(self):
        self.Q = np.zeros((9, 4))

    def init_experiment(self):
        try:
            self.tts = ALProxy("ALTextToSpeech", self.naoIP, self.naoPort)
            self.tts.setLanguage("French")
            self.tts.say("Bonjour tout le monde, je m'appelle Nao !")
            self.tts.say("J'aimerais qu'on apprenne une nouvelle position ensemble !")
        except Exception, e:
            print 'Could not create proxy to ALTextToSpeech'
            print 'Error was: ', e
        try:
            self.postureProxy = ALProxy("ALRobotPosture", self.naoIP, self.naoPort)
        except Exception, e:
            print 'Could not create proxy to ALRobotPosture'
            print 'Error was: ', e
        try:
            self.motionProxy = ALProxy("ALMotion", self.naoIP, self.naoPort)
        except Exception, e:
            print 'Could not create proxy to ALMotion'
            print 'Error was: ', e
        self.motionProxy.wakeUp()
        self.postureProxy.goToPosture("Stand", 0.5)

        self.armController = ArmController(self.naoIP, self.naoPort)
        print "====="
        print "Starting QLearning (Policy %s, Alpha=%f, Gamma=%f" % (self.policy_name, self.alpha, self.gamma),
        if self.policy_name == "epsilon_greedy":
            print ", Epsilon=%f)" % self.epsilon
        else:
            print ")"
        policies = Policies(self.epsilon)
        self.policy = getattr(policies, self.policy_name)
        self.goal_state = random.choice(list(State))
        goal_sentence = "J'aimerais que tu m'apprennes à placer mon bras %s !" % self.goal_state.french_label()
        self.tts.say(goal_sentence)

        print "The Goal State is %s" % self.goal_state.name
        print "====="

    def launch_experiment(self):
        states = list(State)
        states.remove(self.goal_state)
        for i in range(0, self.N):
            state = random.choice(states)
            self.armController.moveToState(state)
            print "Starting Round %d at %s position" % (i, state.name)
            while (state != self.goal_state):
                action = self.policy(state, self.Q[state.position_index()])
                next_state = np.array(state.value)+action.get_2D_offset()
                next_state = State.state_from_array(next_state)
                self.armController.moveToState(next_state)
                print "Moving %s" % action.name

                reward_module.subscribe_to_events()

                while (not(reward_module.value)):
                    time.sleep(1)

                current_reward = reward_module.value
                reward_module.reset()

                current_Q = self.Q[state.position_index(), action.value]
                max_Q = np.amax(self.Q[next_state.position_index()])
                self.Q[state.position_index(), action.value] += self.alpha*(current_reward+self.gamma*max_Q-current_Q)
                state = next_state
                print "Now at %s position (goal %s)" % (state.name, self.goal_state.name)
            print ""
        print self.Q

    def end_experiment(self):
        self.postureProxy.goToPosture("Sit", 0.5)
        self.motionProxy.rest()
