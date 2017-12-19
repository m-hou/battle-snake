"""doc"""

from copy import deepcopy
from board import Entity
from snake import Move

class Game:
    """doc"""
    DISCOUNT_FACTOR = 0.9
    DEPTH = 2

    def __init__(self, board):
        self.board = board

    def best_move(self):
        """doc"""
        possible_moves = self.get_possible_moves(self.board)
        move_evals = {move: self.best_move_helper(self.board.move_snake(self.board.my_snake.id, move), self.DEPTH)
                      for move in possible_moves}
        return max(move_evals.items(), key=lambda x: x[1])[0].get_move()

    def best_move_helper(self, board, depth):
        """doc"""
        if depth == 0:
            return 0
        marked_board = self.flood_fill(board)
        board_eval = self.heuristic(marked_board.my_snake.id, marked_board)
        possible_moves = self.get_possible_moves(marked_board)
        next_boards = [self.other_snakes_next_move(move, deepcopy(board))
                       for move in possible_moves]
        return board_eval + (self.DISCOUNT_FACTOR * max([self.best_move_helper(next_board, depth - 1)
                                                         for next_board in next_boards]))

    def heuristic(self, snake_id, marked_board):
        """stub"""
        if self.board.my_snake.id is snake_id:
            food_x, food_y = self.board.food[0]
            head_x, head_y = self.board.my_snake.head
            return -abs(food_x - head_x) -abs(food_y - head_y)
        else:
            for other_snake in self.board.other_snakes:
                if other_snake.id is snake_id:
                    food_x, food_y = self.board.food[0]
                    head_x, head_y = self.board.other_snake
                    return -abs(food_x - head_x) -abs(food_y - head_y)

    def other_snakes_next_move(self, move, marked_board):
        """stub"""
        other_snake_moves = {}
        for other_snake in marked_board.other_snakes:
            move_evals = {move: self.other_snakes_next_move_helper(other_snake.id, move, marked_board)
                          for move in Move}
            other_snake_moves[other_snake] = max(move_evals.keys(), key=lambda x: x[1])

        for other_snake_move in other_snake_moves:
            marked_board.move_snake(other_snake_move[0], other_snake_move[1])

        return marked_board

    def other_snakes_next_move_helper(self, snake_id, move, marked_board):
        """stub"""
        board = deepcopy(marked_board)
        board.apply_move(snake_id, move)
        return self.heuristic(snake_id, board)


    def flood_fill(self, board):
        """stub"""
        return board

    def get_possible_moves(self, board):
        """stub"""
        all_moves = board.my_snake.range
        other_snakes_all_moves = [cell for other_snakes in board.other_snakes
                                  for cell in other_snakes.range]
        moves = []
        for move, cell in all_moves.items():
            if board.within_bounds(cell) and board.board[cell[1]][cell[0]] in [Entity.FOOD, Entity.EMPTY] and cell not in other_snakes_all_moves:
                moves.append(move)
        return moves
