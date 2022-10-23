# package pong.event

from pong.event.ModelEvent import ModelEvent
from abc import ABC, abstractmethod

"""
    Contract for all classes acting as targets
    for events from model.
    See BreakoutGUI

     *** Nothing to do here ****
"""


class EventHandler(ABC):
    @abstractmethod
    def on_model_event(self, evt: ModelEvent):
        raise NotImplementedError
