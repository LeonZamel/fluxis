from dataclasses import dataclass
from enum import Enum
from typing import Any, NamedTuple, Sequence, Union, List

"""
class BaseDataType(Enum):
    NUMBER: 0
    STRING: 1
    BOOLEAN: 2


class AggregationType(Enum):
    SINGLE: 0
    ARRAY: 1
    TABLE: 2


class DataType(NamedTuple):
    base_type: BaseDataType
    aggregation_type: AggregationType
"""

# Used for constant values


@dataclass
class PortSuggestion:
    how: str  # Should be 'request', 'from_port'
    from_port: str
    getter: str


class PortType(str, Enum):
    OTHER = "other"
    TABLE = "table"
    JSON = "json"
    BOOLEAN = "boolean"
    INT = "int"
    STRING = "string"
    STRING_ARRAY = "string_array"
    ML_MODEL = "ml_model"


@dataclass
class PortConfig:
    key: str
    name: str
    description: str
    required: bool = True
    internal: bool = False
    data_type: str = PortType.OTHER  # Should be one of PortType
    suggestion: PortSuggestion = None


"""
data_type: str  # Should be one of PARAMETER_TYPES
default_value: Any
"""


PortConfigs = List[PortConfig]
