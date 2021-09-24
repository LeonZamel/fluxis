from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig


class Length(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="array",
            name="Array",
            description="Array or other iterable to determine the length of",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="length",
            name="Length",
            description="Length of the input",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        out_ports["length"] = len(in_ports["array"])
