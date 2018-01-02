from enum import Enum
from .cell import Cell


class Move(Enum):
    """
    Move are the possible moves that a snake can make.

    Making a move results in shifting the snake's head by (x, y)
    """

    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

    def get_move(self):
        """Get the name of the move."""
        return self.name.lower()

    def apply_move_to_cell(self, cell):
        """Get the resulting cell from applying a move to a cell."""
        return Cell(self.value[0] + cell.x, self.value[1] + cell.y)


class Snake:
    """
    A snake on the board

    We can assume that a snake has a head and is at least length 3. It's head
    and body can be on the same square (on spawn or after eatting food).
    """

    def __init__(self, snake_data):
        self.taunt = snake_data["taunt"]
        self.name = snake_data["name"]
        self.id = snake_data["id"]
        self.health_points = snake_data["health_points"]
        coords = snake_data["coords"]
        self.head = Cell(*coords[0])
        self.body = [Cell(*coord) for coord in coords]

    def get_possible_moves(self):
        """
        Map of moves that the snake can make and the resulting head cells.

        Note that at least one of these moves will result in death.
        """
        return {move: move.apply_move_to_cell(self.head) for move in Move}

    def apply_move(self, move):
        """
        Applies a move to snake from it's current position.

        When the snake moves, it's head will move forward in the direction and
        all cells will be shifted forward. If the snake grows, it will become 1
        cell longer at it's tail
        """
        self.head = self.get_possible_moves()[move]
        self.body = [self.head] + self.body[:-1]

    def grow(self):
        """
        Grow the snake.

        Adds a cell to the end of the snake (at the same cell as the last cell
        it's body.
        """
        self.body.append(self.body[-1])

    def __len__(self):
        return len(self.body)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash((self.taunt, self.name, self.id, self.health_points, self.head, *self.body))
