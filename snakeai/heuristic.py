import numpy as np
from .common import safe_square_count
from .common import get_travel_distance
from .common import CANT_FIND
from snakemodel.board import EntityId
from snakemodel.cell import Cell


class Heuristic():

    def __init__(self, depth=1):
        self.depth = depth

    DISCOUNT_FACTOR = 0.9
    LARGE_PENALTY = np.array([-1000, 0, 0, 0, 0])
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
        if snake_id in board.dead_snakes.keys():
            return self.LARGE_PENALTY

        snake = board.snakes[snake_id]

        return np.array([
             self._get_tail_dist_penalty(snake, board),
             self._get_open_squares(board, snake),
             self._get_food_score(board, snake),
             # self.scarey_snake_heads(snake, board),
             # self.closest_to_most(snake, board),
        ])

    def closest_to_most(self, snake, board):
        close = 0
        empty_row = [(cell, x, y) for y, row in enumerate(board.board)
                     for x, cell in enumerate(row)
                     if cell == EntityId.EMPTY]

        for (cell, x, y) in empty_row:
            if cell == EntityId.EMPTY:
                closest = min(board.snakes.values(),
                              key=lambda a_snake: a_snake.head.distance(
                                  Cell(x, y)))
                close += closest.id == snake.id
        return close / (len(empty_row) + 1)

    def scarey_snake_heads(self, snake, board):
        other_snakes = [o_snake for o_snake in board.snakes.values()
                        if o_snake.id != snake.id]
        distances = 0
        for osnake in other_snakes:
            distances += snake.head.distance(osnake.head)
        return distances

    def _get_tail_dist_penalty(self, snake, board):
        max_dist_to_tail = self._get_max_dist_from_tail(snake, board)
        travel_distance = get_travel_distance(
                board, snake.head, snake.body[-1])
        tail_dist_penalty = -travel_distance if (
            travel_distance == CANT_FIND) else (
            min(0, max_dist_to_tail - travel_distance))
        return tail_dist_penalty

    def _get_open_squares(self, board, snake):
        reachable_squares = safe_square_count(board, snake.head)
        squares_occupied = len(snake.body)
        if snake.head.distance(snake.body[-1]):
            reachable_squares += squares_occupied
        return reachable_squares

    def _get_food_score(self, board, snake):
        food_evaluation = CANT_FIND
        for food in board.food:
            food_evaluation = min(food_evaluation, food.distance(snake.head))
        length_score = len(snake.body) * self.FOOD_SCORE
        travel_distance = snake.head.distance(snake.body[-1])
        return -food_evaluation + length_score - 100 * (travel_distance == 1)

    def _get_max_dist_from_tail(self, snake, board):
        """Threshold where there is no penalty for being too far from tail."""

        if snake.health_points == self.MAX_HEALTH:
            # this is required or else snake will never eat
            return 1000
        else:
            return 2 + (self.MAX_HEALTH - snake.health_points) / (
                self.MAX_HEALTH) * (board.width + board.height)
