from collections import namedtuple
from .snake_ai import SnakeAI


class GroupAI(SnakeAI):
    """AI to play BattleSnake in a group setting (with more than 2 players)."""

    def best_move(self):
        """
        Make the move that will increase the heuristic the most.

        Avoid all squares that could lead to possible death.
        """
        MoveEvaluation = namedtuple("MoveEvaluation", "move, evaluation")
        move_evals = [
            MoveEvaluation(
                move=candidate_move,
                evaluation=self._get_move_eval(candidate_move)
            )
            for candidate_move in self._get_candidate_moves(
                self.game.you,
                self.game.board)]
        return max(
            move_evals,
            key=lambda move_eval: tuple(move_eval.evaluation)).move.get_move()

    def _get_move_eval(self, move):
        """
        Get a move's eval.

        Evaluate from the prespective the snake with snake_id, on the given
        board, according to the heuristic.
        """
        next_board = self.game.simulate_moves(
            self.game.board,
            {self.game.you: move})
        return self.heuristic.heuristic(self.game.you, next_board)
