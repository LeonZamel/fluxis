from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig


class ManualTrigger(NodeFunction):
    is_trigger_node = True
    in_ports_conf = []
    out_ports_conf = [
        PortConfig(
            key="trigger_out",
            name="Trigger",
            description="The trigger signal once manually started",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf, trigger_on_start=True)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        out_ports["trigger_out"] = "trigger"
