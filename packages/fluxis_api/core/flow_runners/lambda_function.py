import json
import os
from datetime import datetime

import requests
from pytz import utc

from core.adapter import build_flow_from_serialized

from fluxis_engine.core.flow import (
    FlowRunEndEvent,
    FlowRunErrorEvent,
    FlowRunStartEvent,
)
from fluxis_engine.core.observer.eventtypes import EventType
from fluxis_engine.core.observer.observer import Observer
from .flow_runner import FlowRunner


class LambdaRunner(FlowRunner):
    def __init__(self, serialized_flow):
        requests.post(
            os.environ.get("LAMBDA_RUN_URL"),
            json=serialized_flow,
            headers={"x-api-key": os.environ.get("LAMBDA_API_KEY")},
        )


def get_aware_time():
    return datetime.utcnow().replace(tzinfo=utc)


"""
def write_output_callback(flowrun, event: NodeRunEndEvent, node_run_db):
    data_store.write_output_for_node(
        flowrun, event.output, event.node_id, node_run_db)


def on_node_run_start_cb(flowrun, event: NodeRunStartEvent):
    core.models.NodeRun.objects.create(node=core.models.Node.objects.get(
        id__exact=event.node_id), flowrun=flowrun, output=None)


def on_node_run_end_cb(flowrun, event: NodeRunEndEvent):
    node_run_db = core.models.NodeRun.objects.filter(
        flowrun=flowrun).get(node_id__exact=event.node_id)
    node_run_db.datetime_end = timezone.now()
    node_run_db.save()
    if event.reason == NodeRunEndReason.DONE:
        thread = threading.Thread(
            target=write_output_callback, args=(flowrun, event, node_run_db))
        thread.start()
"""


def on_flow_run_start_cb(api_key, callback_url, event: FlowRunStartEvent):
    data = {"datetime_start": str(get_aware_time())}
    requests.patch(callback_url, headers={"Authorization": api_key}, json=data)


def on_flow_run_error_cb(api_key, callback_url, event: FlowRunErrorEvent):
    data = {"successful": False, "message": str(event.error)}
    requests.patch(callback_url, headers={"Authorization": api_key}, json=data)


def on_flow_run_end_cb(api_key, callback_url, event: FlowRunEndEvent):
    data = {
        "datetime_end": str(get_aware_time()),
        "node_run_count": event.node_run_count,
    }
    requests.patch(callback_url, headers={"Authorization": api_key}, json=data)


def lambda_handler(event, context):
    serialized_flow = json.loads(event["body"])
    run_id = serialized_flow["run_id"]
    api_key = os.environ.get("API_KEY")
    callback_url = os.environ.get("CALLBACK_URL") + f"{run_id}/"

    g = build_flow_from_serialized(serialized_flow)

    """
    node_run_start_ob = Observer(
        EventType.NODE_RUN_START, lambda e: on_node_run_start_cb(
            db_flowrun, e)
    )
    g.subscribe(node_run_start_ob)

    node_run_end_ob = Observer(
        EventType.NODE_RUN_END, lambda e: on_node_run_end_cb(db_flowrun, e)
    )
    g.subscribe(node_run_end_ob)
    """

    run_start_ob = Observer(
        EventType.FLOW_RUN_START,
        lambda e: on_flow_run_start_cb(api_key, callback_url, e),
    )
    g.subscribe(run_start_ob)

    run_error_ob = Observer(
        EventType.NODE_RUN_ERROR,
        lambda e: on_flow_run_error_cb(api_key, callback_url, e),
    )
    g.subscribe(run_error_ob)

    run_end_ob = Observer(
        EventType.FLOW_RUN_END, lambda e: on_flow_run_end_cb(api_key, callback_url, e)
    )
    g.subscribe(run_end_ob)

    g.run()
