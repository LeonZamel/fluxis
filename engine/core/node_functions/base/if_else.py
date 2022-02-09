from engine.core.node_function import NodeFunction
from engine.core.port_config import PortConfig


class IfElse(NodeFunction):
    name = "If Else"
    in_ports_conf = [
        PortConfig(
            key="condition",
            name="Condition",
            description="True or False value to determine how to proceed",
        )
    ]
    out_ports_conf = [
        PortConfig(
            key="true",
            name="True",
            description="Triggered when true",
        ),
        PortConfig(
            key="false",
            name="False",
            description="Triggered when true",
        ),
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        if in_ports["condition"]:
            out_ports["true"] = "trigger"
        else:
            out_ports["false"] = "trigger"
