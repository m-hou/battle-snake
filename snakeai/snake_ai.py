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
                move=candidate_move,
                evaluation=self._get_move_eval(
                    snake_id,
                    self.game.simulate_moves(
                        board,
                        {snake_id: candidate_move}),
                    depth)
            )
            for candidate_move in self._get_candidate_moves(snake_id, board)]
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

    def _get_candidate_moves(self, snake_id, board):
        """Get moves that will not lead to immediate death."""
        my_snake = board.snakes[snake_id]
        _, possible_head_cells = self._get_snake_next_possible_cells(
            self.game.you,
            board)
        candidate_moves = [move for move in Move]
        for move, head_cell in possible_head_cells.items():
            for other_snake_id in self.game.get_other_snake_ids(snake_id):
                other_body_cell, other_possible_heads = \
                    self._get_snake_next_possible_cells(
                        other_snake_id,
                        board)
                other_snake = board.snakes[other_snake_id]
                if head_cell in other_body_cell or (
                        (head_cell in other_possible_heads and
                         len(other_snake) >= len(my_snake))):
                    candidate_moves.remove(move)
                    break
        return candidate_moves

    def _get_snake_next_possible_cells(self, snake_id, board):
        """Get possible cells that a snake can occupy on the next turn."""
        snake = board.snakes[snake_id]
        next_body_cells = set(snake.body[:-1])
        possible_head_cells = {move: head_cell
                               for move, head_cell in
                               snake.get_possible_moves().items()
                               if head_cell in next_body_cells}
        return next_body_cells, possible_head_cells
