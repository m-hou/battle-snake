from collections import namedtuple
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
            for candidate_move in self.get_candidate_moves(snake_id, board)]
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

    def get_candidate_moves(self, snake_id, board):
        """Moves that will not lead to immediate death from other snakes."""
        _, possible_heads, _ = self._get_possible_snake_transitions(
            self.game.you,
            board)
        safe_transitions = filter(
            lambda possible_head: self._is_possible_head_safe(
                possible_head, snake_id, board),
            possible_heads)
        return [safe_transition.move for safe_transition in safe_transitions]

    def _is_possible_head_safe(self, possible_head, snake_id, board):
        """
        Check if snake is safe against all possible transitions of all snakes.

        Checks if the head cell does not overlap with any other snakes' next
        body cells and their next possible head cells. If it overlaps with a
        possible head cell, check if the snake is longer than the other snake.
        """

        def _could_snake_die_other_snakes_transition(possible_transition):
            """Could snake die from any transition of another snake."""
            head_cell = possible_head.head_cell
            (other_body_cells, other_possible_heads,
             other_snake) = possible_transition
            could_overlap_body = head_cell in other_body_cells
            could_overlap_head = head_cell in [
                other_head_cell.head_cell
                for other_head_cell in other_possible_heads]
            my_snake_longer = len(my_snake) > len(other_snake)
            return not could_overlap_body and not (
                could_overlap_head and not my_snake_longer)

        my_snake = board.snakes[snake_id]
        return all(map(_could_snake_die_other_snakes_transition,
                       [self._get_possible_snake_transitions(
                           other_snake_id, board)
                        for other_snake_id in
                        self.game.get_other_snake_ids(snake_id)]))

    def _get_possible_snake_transitions(self, snake_id, board):
        """Get possible cells that a snake can occupy on the next turn."""
        snake = board.snakes[snake_id]
        body_cells = snake.body[:-1]
        PossibleHeads = namedtuple("PossibleHeads", "move, head_cell")
        possible_heads = [PossibleHeads(move=move,
                                        head_cell=head_cell)
                          for move, head_cell in
                          snake.get_possible_moves().items()
                          if head_cell not in body_cells]
        return body_cells, possible_heads, snake
