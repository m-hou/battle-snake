import numpy as np
from .common import safe_square_count
from .common import get_travel_distance
from .common import voronoi
from .common import CANT_FIND


class Heuristic():

    def __init__(self, depth=1):
        self.depth = depth

    DISCOUNT_FACTOR = 0.9
    LARGE_PENALTY = np.array([-1000000000000, 0, 0, 0])
    FOOD_SCORE = 100
    MAX_HEALTH = 100
    PENALTY = -5000

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
            [self._in_larger_snake_range_penalty(snake, board),
             self._get_tail_dist_penalty(snake, board),
             self._get_open_squares(board, snake),
             self._get_food_score(board, snake)])

    def _in_larger_snake_range_penalty(self, snake, board):
        """Penalty if in the range (next move) of a larger snake."""
        for enemy in board.get_snakes():
            if enemy is not snake and len(enemy) >= len(snake):
                for _, enemy_head in enemy.get_possible_moves().items():
                    if snake.head == enemy_head:
                        return self.PENALTY
        return 0

    def _get_tail_dist_penalty(self, snake, board):
        """Penalty for being too far away from a tail."""

        allowable_tail_dist = self._allowable_tail_dist(snake, board)

        min_so_far = CANT_FIND
        # make the targets the heads instead of the tails so that we
        # can take advanatage of multi-target a-star
        targets = [target.head for target in board.get_snakes()]
        for seeker in board.get_snakes():
            min_dist, head = get_travel_distance(
                board,
                seeker.body[0],
                targets,
                min_so_far)
            if head == snake.head:
                min_so_far = min_dist

        tail_dist_penalty = -min_so_far if (
            min_so_far == CANT_FIND) else (
            min(0, allowable_tail_dist - min_so_far))
        return tail_dist_penalty

    def _get_open_squares(self, board, snake):
        """Total number of reachable squares."""

        reachable_squares = safe_square_count(board, snake.head)
        squares_occupied = len(snake.body)
        return reachable_squares + squares_occupied

    def _get_food_score(self, board, snake):
        """Incentive to approach closest food."""

        food_evaluation, _ = get_travel_distance(board, snake.head, board.food)
        length_score = len(snake.body) * self.FOOD_SCORE
        return -food_evaluation + length_score

    def _allowable_tail_dist(self, snake, board):
        """Threshold where there is no penalty for being too far from tail."""

        if snake.health_points == self.MAX_HEALTH:
            # this is required or else snake will never eat
            return 2 + ((self.MAX_HEALTH - (snake.prev_health - 1)) / (
                self.MAX_HEALTH)) ** 2 * (board.width + board.height) * 4
        else:
            return 2 + ((self.MAX_HEALTH - snake.health_points) / (
                self.MAX_HEALTH)) ** 2 * (board.width + board.height) * 4

    def _scary_snake_head_penalty(self, my_snake, board):
        """Avoid snake heads that are larger."""
        scary_snake_heads = [snake.head for snake in board.get_snakes()
                             if snake != my_snake and
                             len(snake) >= len(my_snake)]
        closest_dist, _ = get_travel_distance(
            board, my_snake.head, scary_snake_heads)
        return closest_dist * self.FOOD_SCORE / 3
