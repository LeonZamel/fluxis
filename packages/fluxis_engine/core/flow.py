import queue
import time
from collections import defaultdict
from logging import getLogger


from .node import Node
from .observer.eventtypes import (
    FlowRunEndEvent,
    FlowRunErrorEvent,
    FlowRunStartEvent,
    NodeRunEndEvent,
    NodeRunErrorEvent,
    NodeRunStartEvent,
)
from .observer.observable import Observable
from .port import InPort, OutPort
from .run_end_reasons import FlowRunEndReason, NodeRunEndReason

logger = getLogger(__name__)


class Flow(Observable):
    def __init__(self):
        super().__init__()
        self.nodes = dict()
        self.edges = defaultdict(lambda: set())
        # edges_backwards is used to efficiently find the sending port for a receiving port
        self.edges_backwards = dict()
        self.nodes_trigger_on_start = set()
        self.queue = queue.Queue()

    def add_node(self, node, id):
        node.id = id
        self.nodes[id] = node
        node.flow = self
        if node.trigger_on_start:
            self.nodes_trigger_on_start.add(id)

    def run(self):
        self.fire(FlowRunStartEvent())
        node_run_count = 0
        error = None
        start_time = time.time()
        """
        for node in self.nodes_trigger_on_start:
            self.add_to_run_queue(self.nodes[node])
        """
        for node in self.nodes.values():
            if not node.in_ports:
                self.add_to_run_queue(node)

        while not self.queue.empty():
            node = self.queue.get()
            self.fire(NodeRunStartEvent(node.id))

            try:
                (output, error) = node.run()
            except Exception as uncaught_error:
                # Error was not caught by function, this should not happen
                error = uncaught_error

            if error:
                self.fire(NodeRunErrorEvent(node.id, error))
                self.fire(NodeRunEndEvent(node.id, None, NodeRunEndReason.ERROR))
                self.fire(FlowRunErrorEvent(error))
                self.fire(FlowRunEndEvent(node_run_count, FlowRunEndReason.ERROR))
                return

            node_run_count += 1
            self.fire(NodeRunEndEvent(node.id, output, NodeRunEndReason.DONE))

        logger.info(
            "Ran "
            + str(node_run_count)
            + " nodes in "
            + str(time.time() - start_time)
            + " seconds"
        )
        self.fire(FlowRunEndEvent(node_run_count, FlowRunEndReason.DONE))

    def send_from_port(self, port, data):
        # Function called when an outport wants to send data to all receiving ports

        receiving_ports = port.node.flow.edges[port]
        for receive_port in receiving_ports:
            # if receive_port not in iterate_functions_ports:
            receive_port.data = data

    def add_to_run_queue(self, node: Node):
        self.queue.put(node)

    def get_node_by_id(self, id):
        return self.nodes[id]

    def add_edge_by_id_key(
        self, from_node_id: str, from_port_key: str, to_node_id: str, to_port_key: str
    ) -> None:
        from_port = self.nodes[from_node_id].out_ports[from_port_key]
        to_port = self.nodes[to_node_id].in_ports[to_port_key]
        self.add_edge(from_port, to_port)

    def add_edge(self, from_port: OutPort, to_port: InPort) -> None:
        if to_port in self.edges_backwards:
            raise ValueError("Input port already connected")

        self.edges[from_port].add(to_port)
        self.edges_backwards[to_port] = from_port

    def add_edge_by_key(
        self, from_node: Node, from_port_key: str, to_node: Node, to_port_key: str
    ) -> None:
        from_port = from_node.out_ports[from_port_key]
        to_port = to_node.in_ports[to_port_key]
        self.add_edge(from_port, to_port)
