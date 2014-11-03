# -*- encoding: UTF-8 -*-

import argparse
from state import State
import numpy as np
import random
import time
from policies import Policies
from armcontroller import ArmController
from naoqi import ALProxy
from reward import Reward
from naoqi import ALBroker

from qlearning import QLearning
import config


reward_module = None

class QLearning(object):
    "QLearning main class"

    def __init__(self):
        self.Q = np.zeros((9, 4))

    def init_experiment(self):
        try:
            self.tts = ALProxy("ALTextToSpeech", self.naoIP, self.naoPort)
            self.tts.setLanguage("French")
            self.tts.say("Bonjour tout le monde, je m'appelle Nao")
            self.tts.say("J'aimerais tant qu'on apprenne une nouvelle position ensemble")
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
        goal_sentence = "J'aimerais que tu m'apprennes à placer mon bras %s" % self.goal_state.french_label()
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
            self.tts.say("Commençons ainsi")
            time.sleep(1)

            while (state != self.goal_state):
                action = self.policy(state, self.Q[state.position_index()])
                next_state = np.array(state.value)+action.get_2D_offset()
                next_state = State.state_from_array(next_state)
                self.armController.moveToState(next_state)
                print "Moving %s" % action.name
                self.tts.say("Comme ça ?")

                reward_module.subscribe_to_events()

                while (not(reward_module.value) and (reward_module.memory.getData("WordRecognized")[1] < 0.4)):
                    time.sleep(1)
                if (reward_module.memory.getData("WordRecognized")[1] >= 0.4 ):
                    reward_module.successReward()

                current_reward = reward_module.value
                if current_reward == 1:
                    self.tts.say("C'est super")
                elif current_reward == -1:
                    self.tts.say("Zut alors")
                reward_module.reset()

                current_Q = self.Q[state.position_index(), action.value]
                max_Q = np.amax(self.Q[next_state.position_index()])
                self.Q[state.position_index(), action.value] += self.alpha*(current_reward+self.gamma*max_Q-current_Q)
                state = next_state
                print "Now at %s position (goal %s)" % (state.name, self.goal_state.name)
            print ""
            self.tts.say("Incroyable, j'ai réussi on dirait")
        print self.Q
        self.tts.say("On a terminé tout le monde. Regarde la matrice Q que j'ai craché à l'écran")

    def show_results(self):
        states = list(State)
        states.remove(self.goal_state)
        policies = Policies(self.epsilon)
        policy = getattr(policies, "optimal")
        for state in states:
            self.armController.moveToState(state)
            current_state = state
            goal_sentence = "Regarde bien comment je vais arriver %s depuis cette position" % self.goal_state.french_label()
            self.tts.say(goal_sentence)
            while (current_state != self.goal_state):
                action = policy(current_state, self.Q[state.position_index()])
                next_state = np.array(current_state.value)+action.get_2D_offset()
                current_state = State.state_from_array(next_state)
                self.armController.moveToState(current_state)
            self.tts.say("Pas mal, hein ?")

    def end_experiment(self):
        self.tts.say("On dirait bien qu'on a terminé, je vais me coucher à présent")
        self.postureProxy.goToPosture("Sit", 0.5)
        self.motionProxy.rest()

qlearning = QLearning()

parser = argparse.ArgumentParser(description='Launches QLearning Experiment with the Nao Robot.')
parser.add_argument("--naoIP", help="IP of the Nao Robot", default=config.nao_ip)
parser.add_argument("--naoPort", help="Port of the Nao Robot", type=int, default=config.nao_port)
parser.add_argument("--alpha", default=0.2, type=float, help='Learning rate (between 0.0 and 1.0)')
parser.add_argument("--gamma", default=0.9, type=float, help='Discount Factor (between 0.0 and 1.0) which trades off the importance of sooner versus later rewards')
parser.add_argument("--epsilon", default=0.1, type=float, help='Epsilon-greedy parameter (between 0.0 and 1.0) giving the probability of picking a random action')
parser.add_argument("--N", default=5, type=int, help='Number of rounds (the initial position of the robot changes after each new round)')
parser.add_argument("--policy", default="epsilon_greedy", choices=['random', 'epsilon_greedy', 'optimal'], help='Picked policy (random or epsilon-greedy)', dest='policy_name')
args = parser.parse_args(namespace=qlearning)

reward_module = Reward("reward_module", "nao_broker", args.naoIP, args.naoPort)

qlearning.init_experiment()
qlearning.launch_experiment()
#qlearning.show_results()
qlearning.end_experiment()
