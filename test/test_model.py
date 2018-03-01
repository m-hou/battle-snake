import unittest
from snakemodel.snake import Move
from test_util import load_game


class TestBoardTransition(unittest.TestCase):
    """Tests for the simulating board transitions."""

    def test_snake_death(self):
        """Test snake dies on next move."""
        curr_game = load_game('test_cases/snake_dead2.json')
        next_game = load_game('test_cases/snake_dead_next2.json')
        me = curr_game.you
        self.assertEqual(
            curr_game.simulate_moves(
                curr_game.board,
                {me: Move.DOWN,
                 curr_game.get_other_snake_ids(me)[0]: Move.RIGHT,
                 curr_game.get_other_snake_ids(me)[1]: Move.DOWN}
            ),
            next_game.board)
