from collections import defaultdict

from .event import Event
from .observer import Observer


class Observable():
    def __init__(self):
        self.observers = defaultdict(list)

    def subscribe(self, observer: Observer):
        self.observers[observer.event_type].append(observer)

    def fire(self, event: Event):
        event.source = self
        for ob in self.observers[event.event_type]:
            ob.callback(event)
