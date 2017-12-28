import numpy as np
from .common import flood_fill


class Heuristic():

    DISCOUNT_FACTOR = 0.9
    DEPTH = 1
    LARGE_PENALTY = np.array([-1000000000000, 0])
    FOOD_SCORE = 100

    def heuristic(self, snake_id, board):
        """
        A heuristic to evaluate the board.

        Evaluate from the prespective of the snake with snake_id.
        """
        if snake_id in [dead_snake_id
                        for dead_snake_id, _ in board.dead_snakes.items()]:
            return self.LARGE_PENALTY

        snake = board.snakes[snake_id]

        reachable_squares = flood_fill(board, snake.head)
        squares_occupied = len(set(snake.body))

        evaluation = 0
        for food in board.food:
            evaluation += self.FOOD_SCORE / (snake.head.distance(food)**2 + 1)
        evaluation += len(board.snakes[snake_id].body) * self.FOOD_SCORE
        return np.array([reachable_squares + squares_occupied, evaluation])
