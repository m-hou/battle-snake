"""doc"""

from enum import Enum
from snake import Snake

class Entity(Enum):
    """doc"""

    EMPTY = 0
    MY_HEAD = 1
    MY_BODY = 2
    OTHER_HEAD = 3
    OTHER_BODY = 4
    WALL = 5
    FOOD = 6

class Board:
    """doc"""

    def __init__(self, data):
        self.width = data["width"]
        self.height = data["height"]
        self.food = self.find_food(data)
        self.my_snake = self.find_my_snake(data)
        self.other_snakes = self.find_other_snakes(data)
        self.board = self.build_board()

    def find_food(self, data):
        """doc"""
        return [tuple(food) for food in data["food"]]

    def find_my_snake(self, data):
        """doc"""
        return Snake(next(snake
                          for snake in data["snakes"]
                          if snake["id"] == data["you"]))

    def find_other_snakes(self, data):
        """doc"""
        other_snake_ids = [snake_id
                           for snake_id in data["snakes"]
                           if snake_id != data["you"]]
        return {snake["id"]: Snake(snake)
                for snake in data["snakes"]
                if snake["id"] in other_snake_ids}

    def build_board(self):
        """doc"""
        board = [[Entity.EMPTY for _ in range(self.width + 1)] for _ in range(self.height + 1)]
        for x, y in self.food:
            board[y][x] = Entity.FOOD

        for x, y in self.my_snake.body:
            board[y][x] = Entity.MY_BODY

        head_x, head_y = self.my_snake.head
        board[head_y][head_x] = Entity.MY_HEAD

        for other_snake in self.other_snakes:
            for x, y in other_snake.body:
                board[y][x] = Entity.OTHER_BODY

            head_x, head_y = other_snake.head
            board[head_y][head_x] = Entity.OTHER_HEAD
        return board

    def within_bounds(self, cell):
        """doc"""
        return 0 <= cell[0] <= self.width and 0 <= cell[1] <= self.height

    def move_snake(self, snake_id, move):
        """stub"""
        if self.my_snake.id is snake_id:
            self.my_snake.move_snake(move)
            return self
        else:
            for other_snake in self.other_snakes:
                if other_snake.id is snake_id:
                    other_snake.move_snake(move)
                    return self
