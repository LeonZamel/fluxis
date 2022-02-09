from dataclasses import dataclass
from enum import Enum
from typing import Any, NamedTuple, Sequence, Union, List


class ParameterType(str, Enum):
    BOOLEAN = "boolean"
    INT = "int"
    STRING = "string"


@dataclass
class ParameterConfig:
    key: str
    name: str
    description: str
    data_type: str  # Should be one of PARAMETER_TYPES
    default_value: Any
    required: bool = False
    choices: Any = None


ParameterConfigs = List[ParameterConfig]
