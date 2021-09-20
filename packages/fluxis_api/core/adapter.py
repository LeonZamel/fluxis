import io
import os
import threading

import requests
from django.conf import settings
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

import core.data_store as data_store
import core.flow_runners.thread_runner as thread_runner
import core.models as db_models
from fluxis_engine.core.node_functions.node_functions import NODE_CATEGORIES, NODE_FUNCTIONS
from fluxis_engine.core.observer.observer import Observer
from fluxis_engine.core.parameter_config import ParameterType
from fluxis_engine.core.port_config import PortType
from fluxis_engine.core.run_end_reasons import FlowRunEndReason, NodeRunEndReason
from authentication.services.oauth2.oauth2_providers import OAUTH2_PROVIDERS
from authentication.utils import token_expired


from .flow_runners.thread_runner import thread_runner

# TODO: Add port names

# "timer": (TimerFunction, "Timer"),
# "iterate": (IterateFunction, "Iterate over array"),
# "combine_to_array_while": (CombineToArrayWhileFunction, "Combine values to array"),
# "internal_data_http_endpoint": (InternalDataHttpEndpointFunction, "Data from http endpoint"),
# "print": (PrintFunction, "Print value"),


def get_function(name):
    return NODE_FUNCTIONS[name][0]


# Must be a tuple of Actual value, human readable value
PARAMETER_TYPE_CHOICES = [
    (param_type.value, param_type.value) for param_type in ParameterType
]

PORT_TYPE_CHOICES = [(port_type.value, port_type.value) for port_type in PortType]


NODE_FUNCTIONS_CHOICES = [(f[0], f[1][1]) for f in NODE_FUNCTIONS.items()]

NODE_FUNCTIONS_DEFINITIONS = {
    f[0]: {
        "name": f[1][1],
        "is_trigger_node": f[1][0].is_trigger_node,
        "in_ports": list(filter(lambda port: not port.internal, f[1][0].in_ports_conf)),
        "out_ports": list(
            filter(lambda port: not port.internal, f[1][0].out_ports_conf)
        ),
        "parameters": f[1][0].parameters,
        "credentials": f[1][0].credentials,
        "category": f[1][2].value,
    }
    for f in NODE_FUNCTIONS.items()
}


CATEGORICAL_NODE_FUNCTIONS_DEFINITIONS = {cat.value: {} for cat in NODE_CATEGORIES}
for func_key, func in NODE_FUNCTIONS_DEFINITIONS.items():
    CATEGORICAL_NODE_FUNCTIONS_DEFINITIONS[func["category"]][func_key] = func


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
        FullOAuth2CredentialsSerializer,
        DatabaseCredentialsSerializer,
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

    # Run the flow
    if settings.USE_LAMBDA:
        requests.post(
            os.environ.get("LAMBDA_RUN_URL"),
            json=serialized_flow,
            headers={"x-api-key": os.environ.get("LAMBDA_API_KEY")},
        )
    else:
        thread_runner(serialized_flow, db_flowrun_id)
