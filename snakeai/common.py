from snakemodel.board import EntityId
from snakemodel.snake import Move


def flood_fill(board, cell):
    """Count of safe squares that can be reached from cell."""
    visited = set()
    count = 0
    to_visit = [cell]
    while to_visit:
        curr_cell = to_visit.pop()
        if (curr_cell not in visited
                and board.cell_within_bounds(curr_cell)
                and (board.get_entity_at_cell(curr_cell) in
                     [EntityId.EMPTY, EntityId.FOOD]
                     or curr_cell == cell)):
            count += 1
            for move in Move:
                to_visit.append(move.apply_move_to_cell(curr_cell))
        visited.add(curr_cell)
    return count
