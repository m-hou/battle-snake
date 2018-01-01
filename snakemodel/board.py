from itertools import chain
from enum import Enum
from .snake import Snake
from .cell import Cell


class EntityId(Enum):
    """EntityId is a flag that marks what Entity type is currently on a cell"""

    EMPTY = "EMPTY"
    HEAD = "HEAD"
    BODY = "BODY"
    FOOD = "FOOD"


class Board:
    """
    The state of the game board including the food and Snakes.

    Has a grid representation that is a view of the entities on the board.
    """

    def __init__(self, data):
        self.game_id = data["game_id"]
        self.width = data["width"]
        self.height = data["height"]
        self.food = self._create_food(data["food"])
        self.snakes = self._create_snakes(data["snakes"])
        self.dead_snakes = self._create_dead_snakes(data["dead_snakes"])
        self._build_grid()

    def _create_food(self, food_data):
        """Parse food from food_data."""
        return set(Cell(*food) for food in food_data)

    def _create_snakes(self, snakes_data):
        """Parse snakes from snakes_data."""
        return {snake_data["id"]: Snake(snake_data)
                for snake_data in snakes_data}

    def _create_dead_snakes(self, dead_snakes_data):
        """Parse dead snakes from dead_snakes_data."""
        return {dead_snake_data["id"]: Snake(dead_snake_data)
                for dead_snake_data in dead_snakes_data}

    def _build_grid(self):
        """Build a grid of EntityId that represents the current board state."""
        self.board = [[EntityId.EMPTY for _ in range(
            self.width)] for _ in range(self.height)]

        # Mark food
        for cell in self.food:
            self._set_entity_at_cell(cell, EntityId.FOOD)

        # Mark live snakes
        for _, snake in self.snakes.items():
            for cell in snake.body:
                self._set_entity_at_cell(cell, EntityId.BODY)
            self._set_entity_at_cell(snake.head, EntityId.HEAD)

    def is_snake_id_at_cell(self, snake_id, cell):
        """Return True if Entity at Cell is a Snake and has snake_id."""
        for snake in self.get_snakes():
            if snake.id == snake_id:
                return cell in snake.head + snake.body
        return False

    def get_entity_at_cell(self, cell):
        """Get EntityId at Cell."""
        return self.get_entity_at_pos(cell.x, cell.y)

    def get_entity_at_pos(self, x, y):
        """Get EntityId at position."""
        return self.board[y - 1][x - 1]

    def get_object_at_cell(self, cell):
        """Get object at Cell."""
        return self.get_object_at_pos(cell.x, cell.y)

    def get_object_at_pos(self, x, y):
        """Get object at position."""
        entity_at_pos = self.get_entity_at_pos(x, y)
        if entity_at_pos is EntityId.EMPTY:
            return None
        elif entity_at_pos in [EntityId.HEAD, EntityId.BODY]:
            return None
        elif entity_at_pos is EntityId.FOOD:
            return None

    def _set_entity_at_cell(self, cell, entity_id):
        """Set EntityId at Cell."""
        self._set_entity_at_pos(cell.x, cell.y, entity_id)

    def _set_entity_at_pos(self, x, y, entity_id):
        """Set EntityId at position."""
        self.board[y - 1][x - 1] = entity_id

    def cell_within_bounds(self, cell):
        """Return True if Cell is within bounds of the game grid."""
        return self.pos_within_bounds(cell.x, cell.y)

    def pos_within_bounds(self, x, y):
        """Return True if position is within bounds of the game grid."""
        return 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1

    def update_board(self, snake_id_move_mapping):
        """
        State transition for board. Applies moves to all live snakes.

        The Grid is invalidated until the end of this method.
        Order of events:
        1. Move snakes
        2. Snakes dying
        3. Update world
        4. Update grid
        """

        self._move_snakes(snake_id_move_mapping)
        self._resolve_deaths()
        self._update_board_after_move()
        self._build_grid()
        return self

    def _move_snakes(self, snake_id_move_mapping):
        """Apply moves to snakes."""
        for snake_id, move in snake_id_move_mapping.items():
            self.snakes[snake_id].apply_move(move)

    def _resolve_deaths(self):
        """
        Resolve deaths from starvation, wall collision, and snake collision.

        Snakes that die the current turn are moved from snakes to dead_snakes.
        """
        live_snakes = set(snake
                          for snake in self.get_snakes()
                          if snake.health_points > 0 and
                          self.cell_within_bounds(snake.head) and
                          self._check_snake_collision(snake))

        dead_snakes = set(self.get_snakes()) - live_snakes

        self.snakes = {live_snake.id: live_snake
                       for live_snake in live_snakes}

        self.dead_snakes.update({dead_snake.id: dead_snake
                                 for dead_snake in dead_snakes})

    def _check_snake_collision(self, snake):
        """
        Check if snake survived any collisions that occured.

        If the snake collides with a snakes body, it dies. If it collides with
        a snake head that belongs to a snake that is the same or larger length,
        it dies.
        """
        _other_snakes_at_snake_head = self._get_other_snakes_at_snake_head(
            snake)
        if not _other_snakes_at_snake_head:
            return True
        if snake.head in chain.from_iterable(
                [other_snake.body[1:]
                 for other_snake in _other_snakes_at_snake_head]):
            return False

        return self._is_collision_largest_head(
            snake, _other_snakes_at_snake_head)

    def _get_other_snakes_at_snake_head(self, my_snake):
        """Mapping between cells and a list of snakes that occupy that cell."""
        snakes_at_snake_head = []
        for snake in self.get_snakes():
            for cell in snake.body:
                if cell == my_snake.head:
                    snakes_at_snake_head.append(snake)
        snakes_at_snake_head.remove(my_snake)
        return snakes_at_snake_head

    def _is_collision_largest_head(self, snake, other_snakes_at_snake_head):
        """Return True if snake is the longest snake in the collision."""
        return len(snake) > len(max(other_snakes_at_snake_head, key=len))

    def _update_board_after_move(self):
        """
        Update the board after a move.

        Decrement health, grow snakes, remove consumed food, respawn food.
        """
        for snake in self.get_snakes():
            snake.health_points -= 1

        snake_consumed_cell_mapping = self._get_snake_consumed_cell_mapping()
        for snake, food_cell in snake_consumed_cell_mapping.items():
            snake.grow()
            self.food.remove(food_cell)

        for _ in range(len(snake_consumed_cell_mapping)):
            self._spawn_food()

    def _get_snake_consumed_cell_mapping(self):
        """
        Mapping between snakes that consumed food and their head cells.

        We can assume that only one snake will eat the food because if multiple
        snakes tried to eat the same food, at most one of them would survive
        """
        return {snake: snake.head
                for snake in self.get_snakes()
                if snake.head in self.food}

    def get_snakes(self):
        """Return all the live snakes."""
        return [snake for _, snake in self.snakes.items()]

    def _spawn_food(self):
        """stub"""
        pass

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
