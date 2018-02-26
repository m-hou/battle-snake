import unittest
import json
import os
from snakemodel.game import Game
from snakemodel.snake import Move

dir = os.path.dirname(__file__)


class TestBoardTransition(unittest.TestCase):
    """Tests for the simulating board transitions."""

    def test_simple_move(self):
        """Happy flow test."""
        simple_move_file = os.path.join(dir, 'test_cases/simple_move.json')
        simple_move_next_file = os.path.join(
            dir,
            'test_cases/simple_move_next.json')
        with open(simple_move_file, "r") as simple_move, open(
                simple_move_next_file, 'r') as simple_move_next:
            simple_move_game = Game(json.load(simple_move))
            simple_move_next_game = Game(json.load(simple_move_next))
            my_snake_id = simple_move_game.you
            self.assertEqual(
                simple_move_game.simulate_moves(
                    simple_move_game.board,
                    {my_snake_id:
                     Move.RIGHT,
                     simple_move_next_game.get_other_snake_ids(my_snake_id)[0]:
                     Move.DOWN}), simple_move_next_game.board)

    def test_collision(self):
        """Test collision between heads."""
        collision_file = os.path.join(dir, 'test_cases/collision.json')
        collision_next_file = os.path.join(
            dir,
            'test_cases/collision_next.json')
        with open(collision_file, "r") as collision, open(
                collision_next_file, 'r') as collision_next:
            collision_game = Game(json.load(collision))
            collision_next_game = Game(json.load(collision_next))
            my_snake_id = collision_game.you
            self.assertEqual(
                collision_game.simulate_moves(
                    collision_game.board,
                    {my_snake_id:
                     Move.DOWN,
                     collision_game.get_other_snake_ids(my_snake_id)[0]:
                     Move.UP}), collision_next_game.board)

    def test_corner(self):
        """Test transition where snake is at a corner."""
        corner_file = os.path.join(dir, 'test_cases/corner.json')
        corner_next_file = os.path.join(
            dir,
            'test_cases/corner_next.json')
        with open(corner_file, "r") as corner, open(
                corner_next_file, 'r') as corner_next:
            collision_game = Game(json.load(corner))
            collision_next_game = Game(json.load(corner_next))
            my_snake_id = collision_game.you
            self.assertEqual(
                collision_game.simulate_moves(
                    collision_game.board,
                    {my_snake_id:
                     Move.UP,
                     collision_game.get_other_snake_ids(my_snake_id)[0]:
                     Move.DOWN}), collision_next_game.board)

    def test_new_api(self):
        """Test new API."""
        corner_file = os.path.join(dir, 'test_cases/new_api.json')

        with open(corner_file, "r") as corner:
            collision_game = Game(json.load(corner))
            my_snake_id = collision_game.you
            self.assertEqual(
                collision_game.simulate_moves(
                    collision_game.board,
                    {my_snake_id:
                     Move.UP,
                     collision_game.get_other_snake_ids(my_snake_id)[0]:
                     Move.DOWN}), collision_game.simulate_moves(
                    collision_game.board,
                    {my_snake_id:
                     Move.UP,
                     collision_game.get_other_snake_ids(my_snake_id)[0]:
                     Move.DOWN}))
