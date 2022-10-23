from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class Entity:
    """This class represents an Entity in the game. It has a position, a velocity, and a size."""
    x: int
    y: int
    width: int
    height: int
    dx: int = 0
    dy: int = 0

    def move(self):
        """
        This method increments the x and y coordinates of the Entity by the dx and dy values.
        """
        self.x += self.dx
        self.y += self.dy

    def get_x(self) -> int:
        """Returns the x-coordinate of the Entity."""
        return self.x

    def get_y(self) -> int:
        """Returns the y-coordinate of the Entity."""
        return self.y

    def get_center_x(self) -> float:
        return self.x + self.width / 2

    def get_center_y(self) -> float:
        return self.y + self.height / 2

    def get_width(self) -> int:
        """Returns the width of the Entity."""
        return self.width

    def get_height(self) -> int:
        """Returns the height of the Entity."""
        return self.height

    def get_max_x(self) -> int:
        return self.x + self.width

    def get_max_y(self) -> int:
        return self.y + self.height

    def accelerate(self, dx: int, dy: int):
        """
        The accelerate method increments the dx and dy values of the Entity by the values passed in.
        """
        self.dx = dx
        self.dy = dy