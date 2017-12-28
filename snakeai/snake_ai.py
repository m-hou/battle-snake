from collections import namedtuple
from snakemodel.snake import Move
import numpy as np


class SnakeAI():
    """
    An AI to play Battle Snake

    Version 1: Heuristic search, assuming other snakes search with depth of 1
    """

    def __init__(self, game, heuristic):
        self.game = game
        self.heuristic = heuristic

    def best_move(self):
        """
        Get the best move, according to the heuristic.

        Perform recursive search, assuming all other snakes make the best
        immediate move.
        """
        return self._best_move_helper(
            self.game.you, self.game.board, self.heuristic.DEPTH)[0].get_move()

    def _best_move_helper(self, snake_id, board, depth):
        """
        Helper for best_move.

        Get the best move and its eval, for the snake with snake_id, on the
        given board, according to the heuristic, calculated to the given depth.
        Assume other snakes make the best immediate move.
        """
        MoveEvaluation = namedtuple("MoveEvaluation", "move, evaluation")
        move_evals = [
            MoveEvaluation(
                move=possible_move,
                evaluation=self._get_move_eval(
                    snake_id,
                    self.game.simulate_moves(board, {snake_id: possible_move}),
                    depth)
            )
            for possible_move in Move]
        return max(
            move_evals,
            key=lambda move_eval: tuple(move_eval.evaluation))

    def _get_move_eval(self, snake_id, board, depth):
        """
        Get a move's eval.

        Evaluate from the prespective the snake with snake_id, on the given
        board, according to the heuristic, calculated to the given depth.
        Assume other snakes make the best immediate move.
        """
        board_eval = self.heuristic.heuristic(snake_id, board)
        if np.array_equal(board_eval, self.heuristic.LARGE_PENALTY):
            return self.heuristic.LARGE_PENALTY
        if depth <= 1:
            return board_eval
        other_snakes_best_move_mapping = \
            {other_snake_id: self._best_move_helper(snake_id, board, 1).move
             for other_snake_id in self.game.get_other_snake_ids(snake_id)}
        next_board = self.game.simulate_moves(
            board, other_snakes_best_move_mapping)
        return board_eval + self.heuristic.DISCOUNT_FACTOR * \
            self._best_move_helper(
                self.game.you, next_board, depth - 1).evaluation
