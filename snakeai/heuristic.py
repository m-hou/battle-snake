import numpy as np
from .common import safe_square_count
from .common import get_travel_distance


class Heuristic():

    DISCOUNT_FACTOR = 0.9
    DEPTH = 1
    LARGE_PENALTY = np.array([-1000000000000, 0, 0])
    FOOD_SCORE = 100
    MAX_HEALTH = 100

    def heuristic(self, snake_id, board):
        """
        A heuristic to evaluate the board.

        Evaluate from the prespective of the snake with snake_id.
        """

        # LARGE_PENALTY if move will kill snake
        if snake_id in [dead_snake_id
                        for dead_snake_id, _ in board.dead_snakes.items()]:
            return self.LARGE_PENALTY

        snake = board.snakes[snake_id]

        reachable_squares = safe_square_count(board, snake.head)
        squares_occupied = len(set(snake.body))

        food_evaluation = 0
        for food in board.food:
            food_evaluation += \
                self.FOOD_SCORE / (snake.head.distance(food) ** 2 + 1)
        food_evaluation += len(board.snakes[snake_id].body) * self.FOOD_SCORE

        max_dist_to_tail = ((self.MAX_HEALTH - snake.health_points) /
                            self.MAX_HEALTH * (board.width + board.height) + 2)
        dist_from_tail_penalty = min(
            0,
            -(get_travel_distance(board, snake.head, snake.body[-1]) -
              max_dist_to_tail))

        return np.array(
            [dist_from_tail_penalty,
             reachable_squares + squares_occupied,
             food_evaluation])
