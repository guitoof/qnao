from action import Action
import numpy as np
import random

class Policies(object):
    "QLearning main class"
    def __init__(self, epsilon=1.0):
      self.epsilon = epsilon
    def random(self, state, QRow):
        possibleActions = Action.possible_actions(state)
        return random.choice(possibleActions)
    def epsilon_greedy(self, state, QRow):
        if (random.random() < self.epsilon):
          return self.random(state, QRow)
        possible_actions_indexes = [action.value for action in Action.possible_actions(state)]
        filtered_q = {i:QRow[i] for i in possible_actions_indexes}
        optimal_action_indexes = [k for k in filtered_q.keys() if filtered_q[k] == max(filtered_q.values())]
        return Action(random.choice(optimal_action_indexes))
