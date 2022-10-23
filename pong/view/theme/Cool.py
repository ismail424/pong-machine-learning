# package pong.view.theme

from pong.model.Ball import Ball
from pong.model.Paddle import Paddle
from pong.view.Assets import Assets

"""
   Specific theme

   *** Nothing to do here ***
"""


class Cool(Assets):
    # ------------ Handling Images ------------------------
    background = Assets.get_image("coolBg.png")
    
    def __init__(self) -> None:
        super().__init__()
        Assets.bind(Ball, "coolBall.png")
        Assets.bind(Paddle, "coolbluepaddle.png")

    @classmethod
    def get_background(cls):
        return cls.background

    # -------------- Audio handling -----------------------------
