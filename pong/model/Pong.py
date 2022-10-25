# package pong.model
from math import *
from typing import List, Optional, Tuple
import random
from pong.event.EventBus import EventBus
from pong.event.ModelEvent import ModelEvent
from pong.model.Ball import Ball
from pong.model.Config import *
from pong.model.Entity import Entity
from pong.model.Paddle import Paddle

class Pong:
    """
     * Logic for the Pong Game
     * Model class representing the "whole" game
     * Nothing visual here
    """
    points_left  = 0
    points_right = 0
    left_hits    = 0
    right_hits   = 0
    entities: List[Entity]

    # --------  Game Logic -------------

    last_hit: str = ""

    @classmethod
    def load_entities(cls):
        """Loads all entities of the game."""
        right_border_x = GAME_WIDTH - PADDLE_WIDTH
        side_border_y = GAME_HEIGHT / 2 - PADDLE_HEIGHT / 2
        # Initialise entities
        cls.left_paddle = Paddle(0, side_border_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        cls.right_paddle = Paddle(right_border_x, side_border_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        cls.ball = cls.__create_ball()
        cls.entities = [
            cls.left_paddle,
            cls.right_paddle,
            cls.ball
        ]

    @classmethod
    def update(cls):
        """Updates the state of all loaded Entities."""
        for entity in cls.entities:
            entity.move()

        cls.check_collisions()
        
    @classmethod
    def get_points_left(cls) -> int:
        """Returns the points of the left Paddle."""
        return cls.points_left

    @classmethod
    def get_points_right(cls) -> int:
        """Returns the points of the right Paddle."""
        return cls.points_right

    @classmethod
    def get_hits(cls) -> Tuple[int, int]:
        """ Returns the number of hits of both paddles."""
        return cls.left_hits, cls.right_hits

    @classmethod
    def check_collisions(cls):
        """Checks for collisions."""
        # Collision with top and bottom wall
        if cls.last_hit != "top_wall" or cls.last_hit != "bottom_wall":
            cls.__bounce_wall()
        # Collisions between ball & paddle
        if cls.last_hit != "left_paddle" or cls.last_hit != "right_paddle":
            cls.__bounce_paddle()
        
        # Collision with side wall, point scoring
        cls.__touch_down()

    @classmethod
    def reset_points(cls):
        """Resets the game points."""
        cls.points_left = 0
        cls.points_right = 0
        cls.reset_hits()

    
    @classmethod
    def reset_hits(cls):
        """ Resets the hits of both paddles."""
        cls.left_hits = 0
        cls.right_hits = 0
    
    @classmethod
    def get_winner(cls) -> Optional[int]:
        """Returns the winner, if any."""
        if cls.points_left >= MAX_POINTS:
            return 1
        elif cls.points_right >= MAX_POINTS:
            return 2
        else:
            return None
    
    # ------- Helpers --------------------------------------

    @classmethod
    def __touch_down(cls):
        """
        If the ball touches the left or right wall, the points are updated and the ball is reset.
        """
        if (cls.ball.get_center_x() <= 0):
            cls.__point_won("r")
        elif (cls.ball.get_center_x() >= GAME_WIDTH):
            cls.__point_won("l")

        
        
    @classmethod
    def __point_won(cls, side: str):
        """Adds a point to the player on the given side, and resets the ball."""
        if side == "r":
            cls.points_right += 1
        elif side == "l":
            cls.points_left += 1
            
        cls.reset_hits()
        cls.load_entities()

    @classmethod
    def __bounce_wall(cls):
        """If the ball hits the top or bottom of the screen, reverse its vertical direction."""
        if (cls.ball.get_max_y() >= GAME_HEIGHT or cls.ball.get_y() <= 0):
            cls.ball.accelerate(cls.ball.dx, -cls.ball.dy)
            cls.last_hit = "top_wall" if cls.ball.get_y() <= 0 else "bottom_wall"

    @classmethod
    def __bounce_paddle(cls):
        """If the ball hits the paddle, bounce it back at a different angle depending on where it hits the paddle."""
        for paddle in [cls.right_paddle, cls.left_paddle]:
            if cls.ball.intersects(paddle):
                if paddle == cls.right_paddle:
                    cls.right_hits += 1 if cls.last_hit != "right_paddle" else 0
                    cls.change_last_hit("right_paddle")
                else:
                    cls.left_hits += 1 if cls.last_hit != "left_paddle" else 0
                    cls.change_last_hit("left_paddle")

                new_dx, new_dy = cls.__compute_new_vector(paddle)
                cls.ball.accelerate((BALL_SPEED_FACTOR * new_dx), new_dy)
                EventBus.publish_type(ModelEvent.EventType.BALL_HIT_PADDLE)

    @classmethod
    def __create_ball(cls) -> Ball:
        """Creates a ball object with a diffrent starting direction each round."""
        random_dx = random.choice([-4, 4])
        random_dy = random.choice([-1, 1])
        return Ball(
            x = GAME_WIDTH / 2 - BALL_WIDTH / 2,
            y = GAME_HEIGHT / 2 - BALL_HEIGHT / 2,
            width = BALL_WIDTH,
            height = BALL_HEIGHT,
            dx = random_dx,
            dy = random_dy
        )

    @classmethod
    def change_last_hit(cls, item: str):
        """Changes the time of the last hit."""
        cls.last_hit = item

    @classmethod
    def __compute_new_vector(cls, paddle: Entity) -> Tuple[float, float]:
        """Calculates required speed of respective vector for new angle while keeping total speed constant."""
        total_speed = sqrt(cls.ball.dx**2 + cls.ball.dy**2)
        new_angle = cls.__calc_new_angle(paddle)
        
        new_dx = total_speed * cos(new_angle[0])
        new_dy = total_speed * sin(new_angle[0])

        if paddle == cls.left_paddle:
        # Convert general formula to depend on which paddle side new_dx = new_dx * (-1 if new_dx <= 0 else 1)
            new_dy = new_dy * (-1 if new_dy <= 0 else 1)
        else:
            new_dx = new_dx * (-1 if new_dx >= 0 else 1)
            new_dy = new_dy * (-1 if new_dy >= 0 else 1)

        # Ensure the ball's direction is correct when the ball hits different halves of the paddle
        if new_angle[1] <= 0:
           new_dy *= -1

        if cls.ball.get_x() <= GAME_WIDTH / 2:
            new_dy *= -1
            
        if abs(new_dy) == 0:
            new_dy = 0.05
        new_dy += random.uniform(-0.1, 0.1)
        new_dx += random.uniform(-0.1, 0.1)
        return new_dx, new_dy

    @classmethod
    def __calc_new_angle(cls, paddle: Entity) -> Tuple[float, float]:
        """Calculates the new angle of the ball after hitting the paddle."""
        paddle_center_y = paddle.get_y() + paddle.height / 2
        ball_center_y = cls.ball.get_y() + cls.ball.height / 2
        hit_distance = paddle_center_y - ball_center_y

        angle = hit_distance / (paddle.height / 2) * 40
        return [radians(angle), hit_distance]