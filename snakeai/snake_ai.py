from collections import namedtuple
import numpy as np

MoveEvaluation = namedtuple("MoveEvaluation", "move, evaluation")
PossibleHeads = namedtuple("PossibleHeads", "move, head_cell")


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
            self.game.you, self.game.board, self.heuristic.depth).move.get_move()

    def _best_move_helper(self, snake_id, board, depth):
        """
        Helper for best_move.

        Get the best move and its eval, for the snake with snake_id, on the
        given board, according to the heuristic, calculated to the given depth.
        Assume other snakes make the best immediate move.
        """
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

        x = np.array([move.evaluation for move in move_evals])
        best_move = np.amax(x, axis=0)
        best_move = max(
            move_evals,
            key=lambda x: np.array_equal(x.evaluation, best_move))
        return best_move

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

        other_snakes_best_move_mapping = {
            other_snake_id: self._best_move_helper(
                other_snake_id, board, depth - 1).move
            for other_snake_id in self.game.get_other_snake_ids(snake_id)
        }
        next_board = self.game.simulate_moves(
            board, other_snakes_best_move_mapping)

        # Return the board_evaluation plus recursive steps
        return board_eval + self.heuristic.DISCOUNT_FACTOR * (
            self._best_move_helper(self.game.you,
                                   next_board, depth - 1).evaluation)

    def get_candidate_moves(self, snake_id, board):
        """Moves that will not lead to immediate death from other snakes."""
        _, possible_heads, _ = self._get_possible_snake_transitions(
            self.game.you,
            board)

        return [transition.move for transition in possible_heads
                if self._is_possible_head_safe(transition, snake_id, board)]

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
            return not could_overlap_body

        return board.cell_within_bounds(possible_head.head_cell) and (
               all(map(_could_snake_die_other_snakes_transition,
                       [self._get_possible_snake_transitions(
                           other_snake_id, board)
                        for other_snake_id in
                        self.game.snake_ids])))

    def _get_possible_snake_transitions(self, snake_id, board):
        """Get possible cells that a snake can occupy on the next turn."""
        if snake_id in board.dead_snakes:
            return [], [], board.dead_snakes[snake_id]
        snake = board.snakes[snake_id]

        body_cells = snake.body[:-1]
        possible_heads = [PossibleHeads(move=move,
                                        head_cell=head_cell)
                          for move, head_cell in
                          snake.get_possible_moves().items()
                          if head_cell not in body_cells]
        return body_cells, possible_heads, snake
