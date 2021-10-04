import logging
import threading

from core.adapter import build_flow_from_serialized
import core.data_store as data_store
import core.models
from django.utils import timezone
from fluxis_engine.core.observer.eventtypes import (
    EventType,
    FlowRunEndEvent,
    FlowRunErrorEvent,
    FlowRunStartEvent,
    NodeRunEndEvent,
    NodeRunErrorEvent,
    NodeRunStartEvent,
)
from fluxis_engine.core.observer.observer import Observer
from fluxis_engine.core.run_end_reasons import FlowRunEndReason, NodeRunEndReason


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
    def __init__(self, serialized_flow):
        self.run(serialized_flow)

    def run(self, serialized_flow):
        db_flowrun = core.models.FlowRun.objects.get(pk=serialized_flow["run_id"])
        g = None
        try:
            g = build_flow_from_serialized(serialized_flow)
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
