from enum import Enum


class NodeRunEndReason(Enum):
    ERROR = 0
    DONE = 1  # Successful complete node run


class FlowRunEndReason(Enum):
    ERROR = 0
    DONE = 1  # When there are no runnable nodes left
