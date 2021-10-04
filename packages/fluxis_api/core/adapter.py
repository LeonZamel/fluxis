import io
import os
import threading
from collections import Counter
import importlib

import requests
from authentication.services.oauth2.oauth2_providers import OAUTH2_PROVIDERS
from authentication.utils import token_expired
from django.conf import settings
from fluxis_engine.core.node_functions.node_functions import (
    NODE_FUNCTIONS,
)
from fluxis_engine.core.observer.observer import Observer
from fluxis_engine.core.parameter_config import ParameterType
from fluxis_engine.core.port_config import PortType
from fluxis_engine.core.run_end_reasons import FlowRunEndReason, NodeRunEndReason
from fluxis_engine.core.flow import Flow
from fluxis_engine.core.node import Node
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

import core.data_store as data_store
import core.models as db_models


# Must be a tuple of Actual value, human readable value
PARAMETER_TYPE_CHOICES = [
    (param_type.value, param_type.value) for param_type in ParameterType
]

PORT_TYPE_CHOICES = [(port_type.value, port_type.value) for port_type in PortType]


ALL_IMPORTED_NODE_FUNCTIONS = NODE_FUNCTIONS


NODE_FUNCTIONS_DEFINITIONS = {f.name: f for f in ALL_IMPORTED_NODE_FUNCTIONS}


all_names = list(map(lambda f: f.name, NODE_FUNCTIONS_DEFINITIONS.values()))
(most_key, most_count), *rest = Counter(all_names).most_common()
assert most_count <= 1, f"Node function name '{most_key}' exists {most_count} times!"


NODE_FUNCTIONS_CHOICES = [
    (nf.name, nf.name) for nf in NODE_FUNCTIONS_DEFINITIONS.values()
]


def get_node_function(key):
    return NODE_FUNCTIONS_DEFINITIONS[key]


def refresh_flow_oauth2credentials(flow) -> None:
    # Helper method to refresh all the credentials for a flow
    db_credentials = list(
        filter(lambda x: x is not None, [node.credentials for node in flow.nodes.all()])
    )

    # Check credentials and revalidate them if needed
    for creds in db_credentials:
        if hasattr(creds, "refresh_token"):
            refresh_oauth2credentials(creds)


def refresh_oauth2credentials(creds):
    if token_expired(creds.token, 600):  # 10 Minute buffer
        creds_id = creds.id
        new_token = OAUTH2_PROVIDERS[creds.service]().refresh_token(creds.refresh_token)
        creds.token = new_token
        creds.refresh_token = new_token["refresh_token"]
        creds.access_token = new_token["access_token"]
        creds.save()


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


def run_flow(db_flowrun_id):
    db_flowrun = db_models.FlowRun.objects.get(pk=db_flowrun_id)
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
    refresh_flow_oauth2credentials(db_flow)
    refreshed_credentials = list(
        filter(lambda x: x is not None, [node.credentials for node in db_nodes])
    )

    # Serialize to python dicts with serializable types i.e. str, int, bool
    from authentication.serializers import (
        DatabaseCredentialsSerializer,
        FullOAuth2CredentialsSerializer,
    )

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

    # Get the backend to run the flow with
    module_name, function_name = settings.FLUXIS_RUNNER.rsplit(".", 1)
    runner_module = importlib.import_module(module_name)
    runner = getattr(runner_module, function_name)

    runner(serialized_flow)
