from enum import Enum
import numpy as np


class Action(Enum):
    "Action class for moving (unidirectional)"
    Up = 0
    Down = 1
    Left = 2
    Right = 3

    def get_2D_offset(self):
        if self.value == 0:
            return np.array([1, 0])
        elif self.value == 1:
            return np.array([-1, 0])
        elif self.value == 2:
            return np.array([0, -1])
        else:
            return np.array([0, 1])

    @staticmethod
    def possible_actions(state):
        actions = list(Action)
        if state.vertical_pos == 1:
            actions.remove(Action.Up)
        if state.vertical_pos == -1:
            actions.remove(Action.Down)
        if state.horizontal_pos == 1:
            actions.remove(Action.Right)
        if state.horizontal_pos == -1:
            actions.remove(Action.Left)
        return actions
