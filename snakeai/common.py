import heapq
import sys
from snakemodel.board import EntityId
from snakemodel.snake import Move
from snakemodel.cell import Cell

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


def get_travel_distance(board, start_cell, end_cells, prune=sys.maxsize):
    """
    Get the distance between cells without traversing snake cells.

    Uses a* algorithm.
    """

    def closest_target(cell):
        return min([cell.distance(end_cell) * (2 if board.on_edge(cell) else 1)
                    for end_cell in end_cells])

    visited = set()
    to_visit = [(closest_target(start_cell), start_cell)]
    cost_map = {start_cell: 0}

    while to_visit:
        distance, curr_cell = heapq.heappop(to_visit)
        if cost_map[curr_cell] > prune:
            return CANT_FIND, None
        if curr_cell in end_cells:
            return distance, curr_cell
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
                    (distance_travelled + closest_target(neighbour_cell),
                     neighbour_cell))
                if distance_travelled < cost_map.get(
                    neighbour_cell, CANT_FIND
                ):
                    cost_map[neighbour_cell] = distance_travelled
        visited.add(curr_cell)
    return CANT_FIND, None


def voronoi(my_snake, board):
    """Voronoi"""

    count = 0
    distance_maps = {snake: get_distance_map(board, snake)
                     for snake in board.get_snakes()}
    board_cells = [Cell(x, y)
                   for x in range(board.width)
                   for y in range(board.height)]
    for cell in board_cells:
        if distance_maps[my_snake] == min(
            distance_maps.values(),
            key=lambda dist_map: dist_map.get(cell, CANT_FIND)
        ):
            count += 1
    return 0


def get_distance_map(board, snake):
    visited = set()
    to_visit = [(snake.head, 0)]
    distance_map = {snake.head: 0}

    while to_visit:
        curr_cell, dist = to_visit.pop()
        if (curr_cell not in visited
                and board.cell_within_bounds(curr_cell)
                and (board.get_entity_at_cell(curr_cell) in
                     [EntityId.EMPTY, EntityId.FOOD]
                     or curr_cell == snake.head)):
            distance_map[curr_cell] = dist
            for move in Move:
                to_visit.append((move.apply_move_to_cell(curr_cell), dist + 1))
        visited.add(curr_cell)
    return distance_map
