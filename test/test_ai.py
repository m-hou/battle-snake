import unittest
import json
import os
from snakemodel.game import Game
from snakemodel.snake import Move
from snakeai.snake_ai import SnakeAI
from snakeai.heuristic import Heuristic

dir = os.path.dirname(__file__)


class TestSnakeAI(unittest.TestCase):
    """Tests for SnakeAI logic."""

    def test_one_candidate_move(self):
        """Test get_candidate_moves where there is only 1 available move."""
        one_available_move_file = os.path.join(
            dir,
            'test_cases/one_available_move.json')
        with open(one_available_move_file, "r") as one_available_move:
            game = Game(json.load(one_available_move))
            heuristic = Heuristic()
            snake_ai = SnakeAI(game, heuristic)
            self.assertEqual(
                snake_ai.get_candidate_moves(game.you, game.board),
                [Move.DOWN])

    def test_candidate_move_heads_diagonal(self):
        """Test get_candidate_moves where 2 snakes are diagonally adjacent."""
        diagonal_head_file = os.path.join(
            dir,
            'test_cases/diagonal_head.json')
        with open(diagonal_head_file, "r") as diagonal_head:
            game = Game(json.load(diagonal_head))
            heuristic = Heuristic()
            snake_ai = SnakeAI(game, heuristic)
            self.assertEqual(
                snake_ai.get_candidate_moves(game.you, game.board),
                [Move.DOWN])