from engine.core.node_function import NodeFunction
from engine.core.port_config import PortConfig


class GetObjectValueByKey(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="object", name="Object", description="The object to get the value of"
        ),
        PortConfig(key="key", name="Key", description="The key to get the value by"),
    ]
    out_ports_conf = [PortConfig(key="value", name="Value", description="The value")]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        out_ports["value"] = in_ports["object"][in_ports["key"]]
