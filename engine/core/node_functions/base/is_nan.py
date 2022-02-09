import pandas as pd

from engine.core.node_function import NodeFunction
from engine.core.port_config import PortConfig


class IsNaN(NodeFunction):
    name = "Is NaN"
    in_ports_conf = [
        PortConfig(
            key="values",
            name="Values",
            description="Values to analyze for NaN",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="is_nan",
            name="Is NaN",
            description="True or False value(s) depending on if input was NaN",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        out_ports["is_nan"] = pd.isna(in_ports["values"])
