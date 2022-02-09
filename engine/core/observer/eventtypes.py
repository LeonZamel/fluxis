from enum import Enum
from .event import Event


class EventType(Enum):
    FLOW_RUN_START = 0
    FLOW_RUN_END = 1
    FLOW_RUN_ERROR = 2
    NODE_RUN_START = 3
    NODE_RUN_END = 4
    NODE_RUN_ERROR = 5


class FlowRunStartEvent(Event):
    def __init__(self):
        super().__init__(EventType.FLOW_RUN_START)


class FlowRunEndEvent(Event):
    def __init__(self, node_run_count, reason):
        super().__init__(EventType.FLOW_RUN_END)
        self.node_run_count = node_run_count
        self.reason = reason


class FlowRunErrorEvent(Event):
    def __init__(self, error):
        super().__init__(EventType.FLOW_RUN_ERROR)
        self.error = error


class NodeRunStartEvent(Event):
    def __init__(self, node_id):
        super().__init__(EventType.NODE_RUN_START)
        self.node_id = node_id


class NodeRunEndEvent(Event):
    def __init__(self, node_id, output, reason):
        super().__init__(EventType.NODE_RUN_END)
        self.node_id = node_id
        self.output = output
        self.reason = reason


class NodeRunErrorEvent(Event):
    def __init__(self, node_id, error):
        super().__init__(EventType.NODE_RUN_ERROR)
        self.node_id = node_id
        self.error = error
