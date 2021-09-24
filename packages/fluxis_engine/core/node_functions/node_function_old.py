import abc
from typing import NamedTuple, Sequence, Union, Any

from fluxis_engine.core.parameter_config import ParameterConfigs
from fluxis_engine.core.port_config import PortConfigs
from fluxis_engine.core.credentials_config import CredentialsConfig


class NodeFunction(abc.ABC):
    """
    A NodeFunction defines the function and the parameters it needs
    """

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
