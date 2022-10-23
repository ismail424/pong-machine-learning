# package pong.event

"""
Events passed from model to GUI

*** Nothing to do here ***
"""
from enum import Enum


class ModelEvent:

    # Enumeration of events
    class EventType(Enum):
        BALL_HIT_PADDLE = 0
        BALL_HIT_WALL_CEILING = 1
        NEW_BALL = 2

    def __init__(self, event_type: EventType, data=None):
        self.event_type = event_type
        self.data = data

    def __str__(self):
        return str(self.event_type)
