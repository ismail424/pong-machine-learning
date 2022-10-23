from .Entity import Entity

"""
 * A Ball for the Pong game
 * A model class
"""


class Ball(Entity):
    
    def intersects(self, paddle: Entity) -> bool:
        """Determines if the Ball intersects given Entity."""
        above = paddle.get_max_y() < self.get_y()
        below = paddle.get_y() > self.get_max_y()
        left_of = paddle.get_max_x() < self.get_x()
        right_of = paddle.get_x() > self.get_max_x()
        return not (above or below or left_of or right_of)
