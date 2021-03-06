import heapq
from snakemodel.board import EntityId
from snakemodel.snake import Move

CANT_FIND = 1000000


def safe_square_count(board, cell):
    """
    Count of safe squares that can be reached from cell.

    Uses iterative flood fill (dfs) algorithm with stack.
    """
    visited = set()
    to_visit = [cell]
    count = 0
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


def get_travel_distance(board, start_cell, end_cell):
    """
    Get the distance between cells without traversing snake cells.

    Uses a* algorithm.
    """
    visited = set()
    to_visit = [(start_cell.distance(end_cell), start_cell)]
    cost_map = {start_cell: 0}

    while to_visit:
        distance, curr_cell = heapq.heappop(to_visit)
        if curr_cell == end_cell:
            return distance
        for move in Move:
            if (curr_cell not in visited
                    and board.cell_within_bounds(curr_cell)
                    and (board.get_entity_at_cell(curr_cell) in
                         [EntityId.EMPTY, EntityId.FOOD]
                         or curr_cell == start_cell)):
                neighbour_cell = move.apply_move_to_cell(curr_cell)
                distance_travelled = cost_map[curr_cell] + 1
                heapq.heappush(
                    to_visit,
                    (distance_travelled + neighbour_cell.distance(end_cell),
                     neighbour_cell))
                if distance_travelled < cost_map.get(neighbour_cell, CANT_FIND):
                    cost_map[neighbour_cell] = distance_travelled
        visited.add(curr_cell)
    return CANT_FIND
