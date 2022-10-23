# package pong.event

from pong.event.EventHandler import EventHandler
from pong.event.ModelEvent import ModelEvent


# Service to send events **from model** to GUI
# GUI must know if there has been a collision in the model etc.
# 
# NOTE: Events **from GUI** to model handled by JavaFX events and keyboard listeners etc.
# 
# *** Nothing to do here ****
class EventBus:

    handlers = []
    trace = False

    @classmethod
    def register(cls, handler: EventHandler):
        cls.handlers.append(handler)

    @classmethod
    def unregister(cls, handler: EventHandler):
        cls.handlers.remove(handler)

    @classmethod
    def publish(cls, evt: ModelEvent):
        # Tracking all events
        if cls.trace:
            print(evt)
        for evh in cls.handlers:
            evh.on_model_event(evt)

    @classmethod
    def publish_type(cls, tag: ModelEvent.EventType):
        cls.publish(ModelEvent(tag, None))
