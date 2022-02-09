import logging
import threading

import core.data_store as data_store
import core.models
import core.models as db_models
from django.utils import timezone
from engine.core.flow import Flow
from engine.core.node import Node
from engine.core.node_function import NodeFunction
from engine.core.node_functions.node_functions import NODE_FUNCTIONS
from engine.core.observer.eventtypes import (
    EventType,
    FlowRunEndEvent,
    FlowRunErrorEvent,
    FlowRunStartEvent,
    NodeRunEndEvent,
    NodeRunErrorEvent,
    NodeRunStartEvent,
)
from engine.core.observer.observer import Observer
from engine.core.parameter_config import ParameterType
from engine.core.port_config import PortType
from engine.core.run_end_reasons import FlowRunEndReason, NodeRunEndReason
from api.core.adapter import NODE_FUNCTIONS_DEFINITIONS


def save_output(flowrun, event: NodeRunEndEvent, node_run_db):
    data_store.write_output_for_node(
        flowrun.flow.id, flowrun, event.output, event.node_id, node_run_db
    )


def on_node_run_start_cb(flowrun, event: NodeRunStartEvent):
    node_to_run = core.models.Node.objects.get(id__exact=event.node_id)
    core.models.NodeRun.objects.create(
        node=node_to_run,
        flowrun=flowrun,
        output=None,
        name=node_to_run.name,
        function=node_to_run.function,
    )


def on_node_run_end_cb(flowrun, event: NodeRunEndEvent):
    node_run_db = core.models.NodeRun.objects.filter(flowrun=flowrun).get(
        node_id__exact=event.node_id
    )
    node_run_db.datetime_end = timezone.now()
    node_run_db.save()
    if event.reason == NodeRunEndReason.DONE:
        thread = threading.Thread(
            target=save_output, args=(flowrun, event, node_run_db)
        )
        thread.start()


def on_flow_run_start_cb(flowrun, event: FlowRunStartEvent):
    flowrun.datetime_start = timezone.now()
    flowrun.save()


def on_flow_run_error_cb(flowrun, event: FlowRunErrorEvent):
    flowrun.successful = False
    flowrun.message = str(event.error)
    flowrun.save()


def on_flow_run_end_cb(flowrun, event: FlowRunEndEvent):
    flowrun.datetime_end = timezone.now()
    flowrun.node_run_count = event.node_run_count
    flowrun.save()


from .flow_runner import FlowRunner


class ThreadRunner(FlowRunner):
    def __init__(self, db_flowrun):
        self.run(db_flowrun)

    def build_flow(self, db_flowrun):
        # -- Flow components --
        db_flow = db_flowrun.flow
        db_nodes = db_models.Node.objects.filter(flow__exact=db_flow)
        db_config = db_models.FlowConfig.objects.get(flow__exact=db_flow)

        g = Flow()

        db_node: db_models.Node
        for db_node in db_nodes:
            # Add nodes and set parameters
            params = {}
            if db_node.credentials:
                params.credentials = db_node.credentials.id
            for param in db_node.parameters.all():
                params[param.key] = param.value
            node_function = NODE_FUNCTIONS_DEFINITIONS[db_node.function](**params)

            node = Node(node_function, False)
            g.add_node(node, db_node.id)

            for port in db_models.InPort.objects.filter(node__exact=db_node):
                # Add constant values
                if hasattr(port, "constant_value"):
                    g.get_node_by_id(node.id).in_ports[
                        port.key
                    ].data = port.constant_value.value
                    # g.get_node_by_id(node["id"]).in_ports[port["key"]].locked = True

                # Add edges
                db_edges = db_models.Edge.objects.filter(to_port__exact=port)
                for db_edge in db_edges:
                    g.add_edge_by_id_key(
                        db_edge.from_port.node.id,
                        db_edge.from_port.key,
                        port.node.id,
                        port.key,
                    )
        return g

    def run(self, db_flowrun):
        g = None
        try:
            g = self.build_flow(db_flowrun)
        except Exception as e:
            logging.exception("Couldn't build flow")
            # Couldn't build flow, this should not happen
            db_flowrun.successful = False
            db_flowrun.datetime_start = timezone.now()
            db_flowrun.datetime_end = timezone.now()
            db_flowrun.message = "Internal error. Please contact support"
            db_flowrun.save()
            return

        """
        if db_config.log_node_run:
            runs = []
            node_run_ob = Observer(EventType.NODE_RAN, lambda e: print(e))
            g.subscribe(node_run_ob)
        """

        node_run_start_ob = Observer(
            EventType.NODE_RUN_START, lambda e: on_node_run_start_cb(db_flowrun, e)
        )
        g.subscribe(node_run_start_ob)

        node_run_end_ob = Observer(
            EventType.NODE_RUN_END, lambda e: on_node_run_end_cb(db_flowrun, e)
        )
        g.subscribe(node_run_end_ob)

        run_start_ob = Observer(
            EventType.FLOW_RUN_START, lambda e: on_flow_run_start_cb(db_flowrun, e)
        )
        g.subscribe(run_start_ob)

        run_error_ob = Observer(
            EventType.NODE_RUN_ERROR, lambda e: on_flow_run_error_cb(db_flowrun, e)
        )
        g.subscribe(run_error_ob)

        run_end_ob = Observer(
            EventType.FLOW_RUN_END, lambda e: on_flow_run_end_cb(db_flowrun, e)
        )
        g.subscribe(run_end_ob)

        g.run()
