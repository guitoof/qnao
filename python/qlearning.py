import argparse
from state import State
import numpy as np
import random
from policies import Policies
from armcontroller import ArmController
from naoqi import ALProxy


class QLearning(object):
    "QLearning main class"

    def __init__(self):
        self.Q = np.zeros((9, 4))

    def init_experiment(self):
        self.postureProxy = ALProxy("ALRobotPosture", self.naoIP, self.naoPort)
        except Exception, e:
            print 'Could not create proxy to ALRobotPosture'
            print 'Error was: ', e
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

        print "The Goal State is %s" % self.goal_state.name
        print "====="

    def launch_experiment(self):
        states = list(State)
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
                reward = int(input("Enter a reward: "))
                current_Q = self.Q[state.position_index(), action.value]
                max_Q = np.amax(self.Q[next_state.position_index()])
                self.Q[state.position_index(), action.value] += self.alpha*(reward+self.gamma*max_Q-current_Q)
                state = next_state
                print "Now at %s position (goal %s)" % (state.name, self.goal_state.name)
            print ""
        print self.Q

    def end_experiment(self):
        self.postureProxy.goToPosture("Sit", 0.5)
        self.motionProxy.rest()


def main():
    qlearning = QLearning()

    parser = argparse.ArgumentParser(description='Launches QLearning Experiment with the Nao Robot.')
    parser.add_argument("--naoIP", help="IP of the Nao Robot", default="169.254.51.192")
    parser.add_argument("--naoPort", help="Port of the Nao Robot", type=int, default=9559)
    parser.add_argument("--alpha", default=0.2, type=float, help='Learning rate (between 0.0 and 1.0)')
    parser.add_argument("--gamma", default=0.9, type=float, help='Discount Factor (between 0.0 and 1.0) which trades off the importance of sooner versus later rewards')
    parser.add_argument("--epsilon", default=0.1, type=float, help='Epsilon-greedy parameter (between 0.0 and 1.0) giving the probability of picking a random action')
    parser.add_argument("--N", default=5, type=int, help='Number of rounds (the initial position of the robot changes after each new round)')
    parser.add_argument("--policy", default="epsilon_greedy", choices=['random', 'epsilon_greedy'], help='Picked policy (random or epsilon-greedy)', dest='policy_name')
    args = parser.parse_args(namespace=qlearning)

    qlearning.init_experiment()
    qlearning.launch_experiment()
    qlearning.end_experiment()

if __name__ == "__main__":
    main()
