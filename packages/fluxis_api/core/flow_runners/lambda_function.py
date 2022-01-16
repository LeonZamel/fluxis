import json
import os
from datetime import datetime

import requests
from core.adapter import build_flow_from_serialized
from fluxis_engine.core.flow import (FlowRunEndEvent, FlowRunErrorEvent,
                                     FlowRunStartEvent)
from fluxis_engine.core.observer.eventtypes import EventType
from fluxis_engine.core.observer.observer import Observer
from fluxis_engine.core.run_end_reasons import (FlowRunEndReason,
                                                NodeRunEndReason)
from pytz import utc
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .flow_runner import FlowRunner


# TODO: Fix this

class LambdaRunner(FlowRunner):
    def __init__(self, db_flowrun):
        # -- Flow components --
        db_flow = db_flowrun.flow
        db_nodes = db_models.Node.objects.filter(flow__exact=db_flow)
        db_config = db_models.FlowConfig.objects.get(flow__exact=db_flow)
        all_edges = {}
        for node in db_nodes:
            all_edges[node.id] = {}
            for port in node.out_ports.all():
                # Add edges
                all_edges[node.id][port.id] = db_models.Edge.objects.filter(
                    from_port__exact=port
                )

        # -- Credentials --
        refreshed_credentials = list(
            filter(lambda x: x is not None, [node.credentials for node in db_nodes])
        )

        # Serialize to python dicts with serializable types i.e. str, int, bool
        from authentication.serializers import (
            DatabaseCredentialsSerializer, FullOAuth2CredentialsSerializer)

        serialized_credentials = {}
        for cred in refreshed_credentials:
            serialized_cred = None
            if hasattr(cred, "refresh_token"):
                serialized_cred = FullOAuth2CredentialsSerializer(cred).data
            else:
                serialized_cred = DatabaseCredentialsSerializer(cred).data
            serialized_credentials[str(cred.id)] = serialized_cred

        from core.api.serializers import FlowSerializer

        # JSON renderer and parser to get rid of UUID fields and convert to nested dicts
        serialized_flow = JSONParser().parse(
            io.BytesIO(JSONRenderer().render(FlowSerializer(db_flow).data))
        )

        serialized_flow["run_id"] = str(db_flowrun.id)
        serialized_flow["credentials"] = serialized_credentials

        serialized_flow
        requests.post(
            os.environ.get("LAMBDA_RUN_URL"),
            json=serialized_flow,
            headers={"x-api-key": os.environ.get("LAMBDA_API_KEY")},
        )


def get_aware_time():
    return datetime.utcnow().replace(tzinfo=utc)


def build_flow_from_serialized(serialized_flow: dict):
    flow_id = serialized_flow["id"]
    nodes = serialized_flow["nodes"]
    edges = serialized_flow["edges"]
    credentials = serialized_flow["credentials"]

    g = Flow()

    for node in nodes:
        # Add nodes and set parameters
        params = {}
        if node["credentials"]:
            params["credentials"] = credentials[node["credentials"]["id"]]
        for param in node["parameters"]:
            params[param["key"]] = param["value"]
        node_function = NODE_FUNCTIONS_DEFINITIONS[node["function"]](**params)
        has_trigger_port = node["trigger_port"]
        beNode = Node(node_function, has_trigger_port)
        g.add_node(beNode, node["id"])

        for port in node["in_ports"]:
            # Add constant values
            if port["constant_value"]:
                g.get_node_by_id(node["id"]).in_ports[port["key"]].data = port[
                    "constant_value"
                ]["value"]
                g.get_node_by_id(node["id"]).in_ports[port["key"]].locked = True

    for edge in edges:
        g.add_edge_by_id_key(
            edge["from_port"]["node"],
            edge["from_port"]["key"],
            edge["to_port"]["node"],
            edge["to_port"]["key"],
        )

    return g

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
