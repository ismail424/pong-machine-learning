# package pong.view.theme

from pong.model.Ball import Ball
from pong.model.Paddle import Paddle
from pong.view.Assets import Assets

"""
   Specific theme

   *** Nothing to do here ***
"""


class Duckie(Assets):
    # ------------ Handling Images ------------------------

    background = Assets.get_image("duckieBg.jpg")

    def __init__(self) -> None:
        super().__init__()
        Assets.bind(Ball, "duckieBall.png")
        Assets.bind(Paddle, "coolbluepaddle.png")

    @classmethod
    def get_background(cls):
        return cls.background

    # -------------- Audio handling -----------------------------
