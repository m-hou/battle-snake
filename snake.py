"""doc"""

from enum import Enum

class Move(Enum):
    """doc"""
    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

    def get_move(self):
        """doc"""
        return self.name.lower()

    def apply_move(self, position):
        """doc"""
        return (self.value[0] + position[0], self.value[1] + position[1])

class Snake:
    """doc"""

    def __init__(self, snake):
        self.id = snake["id"]
        self.health = snake["health_points"]
        cells = snake["coords"]
        self.head = tuple(cells[0])
        self.body = [tuple(cell) for cell in cells[1:]]
        self.range = {move: move.apply_move(self.head) for move in Move}

    def move_snake(self, move):
        """doc"""
        self.body = list(self.head) + self.body[:-1]
        self.head = self.range[move]
