# -*- encoding: UTF-8 -*-

from enum import Enum


class State(Enum):
    "Representing a state of the robot"
    UpLeft = (1, -1)
    Up = (1, 0)
    UpRight = (1, 1)
    Left = (0, -1)
    Center = (0, 0)
    Right = (0, 1)
    DownLeft = (-1, -1)
    Down = (-1, 0)
    DownRight = (-1, 1)

    def __init__(self, vertical_pos, horizontal_pos):
        self.vertical_pos = vertical_pos
        self.horizontal_pos = horizontal_pos

    def french_label(self):
        if self == State.UpLeft:
            return "en haut à gauche."
        if self == State.Up:
            return "en haut au milieu."
        if self == State.UpRight:
            return "en haut à droite."
        if self == State.Left:
            return "à gauche."
        if self == State.Center:
            return "au centre."
        if self == State.Right:
            return "à droite."
        if self == State.DownLeft:
            return "en bas à gauche."
        if self == State.Down:
            return "en bas au milieu."
        if self == State.DownRight:
            return "en bas à droite."

    def position_index(self):
        return 3*(-self.vertical_pos+1)+self.horizontal_pos+1

    @staticmethod
    def state_from_array(array):
        states = list(State)
        return [s for s in states if s.vertical_pos == array[0] and s.horizontal_pos == array[1]][0]
