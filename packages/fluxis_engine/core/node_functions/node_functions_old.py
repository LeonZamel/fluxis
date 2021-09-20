import sched
import time
import traceback

import numpy as np
import pandas as pd
import requests
from pushbullet import Pushbullet

from fluxis_engine.core.node_functions.node_function import NodeFunction


# Triggers


class TimerFunction(NodeFunction):
    is_trigger_node = True
    in_ports_conf = {"repetition": "internal:int"}
    out_ports_conf = {"trigger_out": "trigger", "repetition": "int"}
    parameters = {"seconds": "float", "repetitions": "int"}

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        out_ports["trigger_out"] = "trigger"
        out_ports["repetition"] = in_ports["repetition"]


# TODO: Another way to handle internal data?


class InternalDataHttpEndpointFunction(NodeFunction):
    is_trigger_node = True
    in_ports_conf = {"data_in": "internal:any"}
    out_ports_conf = {"data": "any"}

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        out_ports["data"] = in_ports["data_in"]


# Regular Functions


class CustomNodeFunction(NodeFunction):
    def __init__(self, in_ports_conf: set, out_ports_conf: set, function):
        super().__init__(in_ports_conf, out_ports_conf)
        self.function = function

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        self.function(in_ports, out_ports)


class GateFunction(NodeFunction):
    in_ports_conf = {"condition": "boolean", "value_in": "any"}
    out_ports_conf = {"value_out": "any"}

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        if in_ports["condition"]:
            out_ports["value"] = in_ports["value"]


class PrintFunction(NodeFunction):
    in_ports_conf = {"value": "int"}
    out_ports_conf = {}

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        print(in_ports["value"])


class ConstantValueFunction(NodeFunction):
    in_ports_conf = {}
    out_ports_conf = {"value": "any"}
    parameters = []

    def __init__(self, value):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.value = value

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        out_ports["value"] = self.value


# TODO: Add Multiple acceptable types


class IterateFunction(NodeFunction):
    in_ports_conf = {"array": "any[]"}
    out_ports_conf = {"array_element": "any", "index": "int", "last_element": "boolean"}

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.index = -1

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        array = in_ports["array"]
        if self.index == -1:
            if len(array) == 0:
                return
            self.index = len(array) - 1
        out_ports["array_element"] = array[self.index]
        out_ports["index"] = self.index
        self.index -= 1
        if self.index != -1:
            out_ports["last_element"] = False
            in_ports_ref["array"].data = array
        else:
            out_ports["last_element"] = True
            self.index = -1


class CombineToArrayWhileFunction(NodeFunction):
    in_ports_conf = {"element": "any", "stop": "boolean"}
    out_ports_conf = {"array": "any[]"}

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.array = []

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        self.array.append(in_ports["element"])
        if in_ports["stop"]:
            out_ports["array"] = self.array
            self.array = []


class CreateArrayFunction(NodeFunction):
    in_ports_conf = {}
    out_ports_conf = {"array": "any[]"}

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        out_ports["array"] = list()


class AppendToArrayFunction(NodeFunction):
    in_ports_conf = {"array_in": "any[]", "value": "any"}
    out_ports_conf = {"array_out": "any[]"}

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    # (almost) Same code as merge array function
    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        temp = np.append(in_ports["array_in"], in_ports["value"])
        out_ports["array_out"] = temp


class MergeArraysFunction(NodeFunction):
    in_ports_conf = {"array_in_1": "any[]", "array_in_2": "any[]"}
    out_ports_conf = {"array_out": "any[]"}

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    # (almost) Same code as append function
    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        temp = np.append(in_ports["array_in_1"], in_ports["array_in_2"])
        out_ports["array_out"] = temp


class SetArrayValueAtIndexFunction(NodeFunction):
    in_ports_conf = {"array_in": "any[]", "index": "int", "value": "any"}
    out_ports_conf = {"array_out": "any[]"}

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        arr = in_ports["array"]
        arr[in_ports["index"]] = in_ports["value"]
        out_ports["array"] = arr


class GetArrayValueAtIndexFunction(NodeFunction):
    in_ports_conf = {"array": "any[]", "index": "int"}
    out_ports_conf = {"value": "any"}

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        out_ports["value"] = in_ports["array"][in_ports["index"]]


"""
class BinaryMathFunctionsFunction(NodeFunction):
    in_ports_conf = {"operator1": "number", "operator2": "number"}
    out_ports_conf = {"result": "number"}
    parameters = {"function_type": "choice"}
    parameter_choices = {"function_type": (
        "add +", "subtract -", "multiply *", "divide /")}

    def __init__(self, function_type):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.function_type = function_type
        self.exec_functions = {
            "add +": lambda op1, op2: op1 + op2,
            "subtract -": lambda op1, op2: op1 - op2,
            "multiply *": lambda op1, op2: op1 * op2,
            "divide /": lambda op1, op2: op1 / op2,
        }

    def run(self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict):
        out_ports["result"] = self.exec_functions[self.function_type](
            in_ports["operator1"], in_ports["operator2"])
"""
