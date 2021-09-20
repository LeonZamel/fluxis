from fluxis_engine.core.node_functions.node_function import NodeFunction


from fluxis_engine.core.node_functions.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig


class SetObjectValueByKey(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="object_in", name="Object", description="The object to set the value on"
        ),
        PortConfig(key="key", name="Key", description="The key to set the value by"),
        PortConfig(key="value", name="Value", description="The Value to set"),
    ]
    out_ports_conf = [
        PortConfig(
            key="object_out", name="Object", description="The object with the new value"
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        object_in = in_ports["object_in"]
        object_in[in_ports["key"]] = in_ports["value"]
        out_ports["object_out"] = object_in
