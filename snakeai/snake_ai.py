from collections import namedtuple
from snakemodel.snake import Move


class SnakeAIv1():
    """
    An AI to play Battle Snake

    Version 1: Heuristic search, assuming other snakes search with depth of 1
    """

    DISCOUNT_FACTOR = 0.9
    DEPTH = 1
    LARGE_PENALTY = -1000000000000
    FOOD_SCORE = 100

    def __init__(self, game):
        self.game = game

    def best_move(self):
        """
        Get the best move, according to the heuristic.

        Perform recursive search, assuming all other snakes make the best
        immediate move.
        """
        return self._best_move_helper(
            self.game.you, self.game.board)[0].get_move()

    def _best_move_helper(self, snake_id, board, depth=DEPTH):
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
        return max(move_evals, key=lambda move_eval: move_eval.evaluation)

    def _get_move_eval(self, snake_id, board, depth):
        """
        Get a move's eval.

        Evaluate from the prespective the snake with snake_id, on the given
        board, according to the heuristic, calculated to the given depth.
        Assume other snakes make the best immediate move.
        """
        board_eval = self._heuristic(snake_id, board)
        if board_eval == self.LARGE_PENALTY:
            return self.LARGE_PENALTY
        if depth <= 1:
            return board_eval
        other_snakes_best_move_mapping = \
            {other_snake_id: self._best_move_helper(snake_id, board, 1).move
             for other_snake_id in self.game.get_other_snake_ids(snake_id)}
        next_board = self.game.simulate_moves(
            board, other_snakes_best_move_mapping)
        return board_eval + self.DISCOUNT_FACTOR * self._best_move_helper(
            self.game.you, next_board, depth - 1).evaluation

    def _heuristic(self, snake_id, board):
        """
        A heuristic to evaluate the board.

        Evaluate from the prespective of the snake with snake_id.
        """
        if snake_id in [dead_snake_id
                        for dead_snake_id, _ in board.dead_snakes.items()]:
            return self.LARGE_PENALTY

        evaluation = 0
        snake_head = board.snakes[snake_id].head
        for food in board.food:
            evaluation += self.FOOD_SCORE / (snake_head.distance(food)**2 + 1)
        evaluation += len(board.snakes[snake_id].body) * self.FOOD_SCORE
        return evaluation

    def _flood_fill(self, board):
        """stub"""
        raise NotImplementedError
