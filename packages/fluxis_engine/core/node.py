from .node_function import NodeFunction
from .port import InPort, OutPort


class Node(object):
    """
    A Node has a function and the ports for the function. It acts as an adapter to the function it contains
    """

    def __init__(self, function: NodeFunction, optional_trigger_port: bool = False):
        self.id = None
        self.flow = None
        self.function = function
        self.function.node = self
        self.trigger_on_start = function.trigger_on_start
        self.in_ports = dict()
        self.out_ports = dict()

        # Add ports
        for port in function.in_ports_conf:
            if port.key == "trigger":
                raise ValueError(
                    "'trigger' is a reserved port name for the optional trigger port"
                )
            self.in_ports[port.key] = InPort(self)

        if optional_trigger_port:
            self.in_ports["trigger"] = InPort(self)

        for port in function.out_ports_conf:
            self.out_ports[port.key] = OutPort(self)

    def notify_port_state_changed(self):
        """
        Callback when an input port receives data
        """
        if len(self.in_ports) == 0:
            # In case the node has no in_ports we need to prevent an infinite call
            return

        # To run, all input ports must have data
        if all((port.has_data for port in self.in_ports.values())):
            self.flow.add_to_run_queue(self)

    def run(self):
        in_port_data = {key: port.data for (key, port) in self.in_ports.items()}
        out_port_data = {key: None for (key, port) in self.out_ports.items()}

        self.function.pre_run(in_port_data, self.in_ports)
        self.function.run(in_port_data, out_port_data, self.in_ports, self.out_ports)

        for (key, val) in out_port_data.items():
            if val is not None:
                self.out_ports[key].data = val

        return out_port_data
