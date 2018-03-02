import numpy as np
from .common import safe_square_count
from .common import get_travel_distance
from .common import CANT_FIND


class Heuristic():

    def __init__(self, depth=1):
        self.depth = depth

    DISCOUNT_FACTOR = 0.9
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

        return np.array(
            [self._get_tail_dist_penalty(snake, board),
             self._get_open_squares(board, snake),
             self._get_food_score(board, snake)])

    def _get_tail_dist_penalty(self, snake, board):
        max_dist_to_tail = self._get_max_dist_from_tail(snake, board)

        min_so_far = CANT_FIND
        for target in board.get_snakes():
            tail = target.body[-1]
            min_my_dist = min_so_far
            min_other_dist = CANT_FIND
            for seeker in board.get_snakes():
                if seeker == snake:
                    min_my_dist = get_travel_distance(
                        board, seeker.head, tail, min_my_dist)
                else:
                    min_other_dist = get_travel_distance(
                        board,
                        seeker.head,
                        tail,
                        min(min_other_dist, min_my_dist))
            if (min_other_dist > min_my_dist):
                min_so_far = min(min_so_far, min_my_dist)

        tail_dist_penalty = -min_so_far if (
            min_so_far == CANT_FIND) else (
            min(0, max_dist_to_tail - min_so_far))
        return tail_dist_penalty

    def _get_open_squares(self, board, snake):
        reachable_squares = safe_square_count(board, snake.head)
        squares_occupied = len(snake.body)
        return reachable_squares + squares_occupied

    def _get_food_score(self, board, snake):
        food_evaluation = CANT_FIND
        for food in board.food:
            food_evaluation = min(food_evaluation, food.distance(snake.head))
        length_score = len(snake.body) * self.FOOD_SCORE
        return -food_evaluation + length_score

    def _get_max_dist_from_tail(self, snake, board):
        """Threshold where there is no penalty for being too far from tail."""

        if snake.health_points == self.MAX_HEALTH:
            # this is required or else snake will never eat
            return 2 + (self.MAX_HEALTH - snake.prev_health) / (
                self.MAX_HEALTH) * (board.width + board.height)
        else:
            return 2 + (self.MAX_HEALTH - snake.health_points) / (
                self.MAX_HEALTH) * (board.width + board.height)
