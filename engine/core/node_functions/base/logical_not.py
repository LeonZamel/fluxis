import numpy as np

from engine.core.node_function import NodeFunction
from engine.core.port_config import PortConfig


class LogicalNot(NodeFunction):
    name = "Logical Not"
    in_ports_conf = [
        PortConfig(
            key="in",
            name="In",
            description="True or False value(s) to invert",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="out",
            name="Out",
            description="Inverted input",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        out_ports["out"] = np.logical_not(in_ports["in"])
