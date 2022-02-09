

class Observer():
    def __init__(self, event_type, callback):
        self.event_type = event_type
        self.callback = callback
