import abc
from enum import Enum
from inspect import signature
from typing import Any, Callable

from fluxis_engine.core.credentials_config import CredentialsConfig
from fluxis_engine.core.parameter_config import ParameterConfigs
from fluxis_engine.core.port_config import PortConfig, PortConfigs


class NodeFunction(abc.ABC):
    """
    A NodeFunction defines the function and the parameters it needs
    """

    key: str = None
    name: str = ""
    category: str = None
    description: str = ""  # Should be a one sentence description
    explanation: str = ""  # Longer explanation on how to use

    in_ports_conf: PortConfigs = []
    out_ports_conf: PortConfigs = []
    parameters: ParameterConfigs = []
    credentials: CredentialsConfig = None

    # If this function is a trigger node and therefore externally triggered
    is_trigger_node: bool = False

    # TODO: Find clear separation for what goes in node and what in node function
    def __init__(
        self,
        in_ports_conf: PortConfigs,
        out_ports_conf: PortConfigs,
        trigger_on_start=False,
    ):
        self.in_ports_conf = in_ports_conf
        self.out_ports_conf = out_ports_conf
        self.trigger_on_start = trigger_on_start
        self.node = None

    @abc.abstractmethod
    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        """
        Will be the code that will be executed when the corresponding node is run.
        It usually maps input ports to output ports.
        """

    def pre_run(self, in_ports: dict, in_ports_ref: dict):
        pass
        """
        Called before run
        """


def node_function(name: str = None, description: str = None, explanation: str = None):
    """
    Decorator to turn a regular function into a NodeFunction object that can be used by the api.
    """

    name_ = name
    description_ = description
    explanation_ = explanation

    def inner(func):
        class NF(NodeFunction):
            key = func.__name__
            name = name_ or func.__name__
            description = (
                description_ or func.__doc__
            )  # Should be a one sentence description
            explanation = (
                explanation_ or func.__doc__
            )  # Longer explanation on how to use

            in_ports_conf: PortConfigs = []
            out_ports_conf: PortConfigs = []
            parameters: ParameterConfigs = []
            credentials: CredentialsConfig = None

            # If this function is a trigger node and therefore externally triggered
            is_trigger_node: bool = False

            func_sig = signature(func)
            for param_name, parameter in func_sig.parameters.items():
                in_ports_conf.append(
                    PortConfig(key=param_name, name=param_name, description="")
                )

            out_ports_conf.append(PortConfig("output", "Output", ""))

            def __init__(self):
                super().__init__(self.in_ports_conf, self.out_ports_conf)

            def run(
                self,
                in_ports: dict,
                out_ports: dict,
                in_ports_ref: dict,
                out_ports_ref: dict,
            ):
                args = []
                for data in in_ports.values():
                    args.append(data)
                ret = self(*args)
                out_ports["output"] = ret

            def __call__(self, *args):
                ret = func(*args)
                return ret

        return NF

    return inner
