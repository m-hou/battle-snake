import numpy as np
from .common import safe_square_count
from .common import get_travel_distance
from .common import CANT_FIND


class Heuristic():

    DISCOUNT_FACTOR = 0.9
    DEPTH = 1
    LARGE_PENALTY = np.array([-1000000000000, 0, 0])
    FOOD_SCORE = 100
    MAX_HEALTH = 100

    def heuristic(self, snake_id, board):
        """
        A hierarchical heuristic to evaluate the board.

        1st priority - avoid moves that lead to certain death
        2nd priority - chase tail with certain threshold to look for food, if
            can't find food, chase tail as closely as possible
        3rd priority - find tail with certain threshold to look for food
        """

        # LARGE_PENALTY if move will kill snake
        if snake_id in [dead_snake_id
                        for dead_snake_id, _ in board.dead_snakes.items()]:
            return self.LARGE_PENALTY

        snake = board.snakes[snake_id]

        reachable_squares = safe_square_count(board, snake.head)
        squares_occupied = len(snake.body)

        food_evaluation = CANT_FIND
        for food in board.food:
            food_evaluation = min(
                food_evaluation,
                get_travel_distance(board, snake.head, food))
        length_score = len(board.snakes[snake_id].body) * self.FOOD_SCORE

        max_dist_to_tail = self._get_max_dist_from_tail(
            snake, board, food_evaluation)
        travel_distance = get_travel_distance(
                board, snake.head, snake.body[-1])
        dist_from_tail_penalty = -travel_distance if (
            travel_distance == CANT_FIND) else (
            min(0, max_dist_to_tail - travel_distance))

        return np.array(
            [dist_from_tail_penalty,
             reachable_squares + squares_occupied,
             -food_evaluation + length_score])

    def _get_max_dist_from_tail(self, snake, board, food_evaluation):
        """Threshold where there is no penalty for being too far from tail."""

        if snake.health_points == self.MAX_HEALTH:
            return 1000
        elif food_evaluation == CANT_FIND:
            return 2
        else:
            return 2 + (self.MAX_HEALTH - snake.health_points) / (
                self.MAX_HEALTH) * (board.width + board.height)
