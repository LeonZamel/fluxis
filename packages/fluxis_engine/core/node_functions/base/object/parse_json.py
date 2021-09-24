import json

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig


class ParseJSON(NodeFunction):
    in_ports_conf = [
        PortConfig(key="json", name="JSON", description="The JSON text to parse")
    ]
    out_ports_conf = [
        PortConfig(key="object", name="Object", description="The parsed object")
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        out_ports["object"] = json.loads(in_ports["json"])
