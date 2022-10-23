from pong.model.Config import GAME_HEIGHT, PADDLE_HEIGHT
from .Entity import Entity

class Paddle(Entity):
    def move(self):
        # Assert within game border
        if self.dy > 0:
            if self.y >= GAME_HEIGHT - PADDLE_HEIGHT:
                self.dy = 0
        else:
            if self.y <= 0:
                self.dy = 0

        self.x += self.dx
        self.y += self.dy
