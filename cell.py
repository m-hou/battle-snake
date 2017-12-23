class Cell:
    """Cell represents a position on the game grid with coordinates x and y."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def distance(self, other):
        """Calculate the Manhattan distance between cells"""
        return abs(self.x - other.x) + abs(self.y - other.y)
