from fluxis_engine.core.node_functions.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig


class GetObjectKeys(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="object",
            name="Object",
            description="The object to get the keys of",
        )
    ]
    out_ports_conf = [
        PortConfig(
            key="keys",
            name="Keys",
            description="The keys of the object",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        out_ports["keys"] = in_ports["object"].keys()
