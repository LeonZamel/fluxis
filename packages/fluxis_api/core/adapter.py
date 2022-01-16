import importlib
import logging
from collections import Counter

from authentication.services.oauth2.oauth2_providers import OAUTH2_PROVIDERS
from authentication.utils import token_expired
from django.conf import settings
from fluxis_engine.core.flow import Flow
from fluxis_engine.core.node import Node
from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.node_functions.node_functions import NODE_FUNCTIONS
from fluxis_engine.core.observer.observer import Observer
from fluxis_engine.core.parameter_config import ParameterType
from fluxis_engine.core.port_config import PortType

import core.data_store as data_store
import core.models as db_models

logger = logging.getLogger(__name__)

# Must be a tuple of Actual value, human readable value
PARAMETER_TYPE_CHOICES = [
    (param_type.value, param_type.value) for param_type in ParameterType
]

PORT_TYPE_CHOICES = [(port_type.value, port_type.value) for port_type in PortType]


ALL_IMPORTED_NODE_FUNCTIONS = NODE_FUNCTIONS
for path in settings.FLUXIS_NODEFUNCTION_PATHS:
    if not path:
        continue
    spec = importlib.util.spec_from_file_location("module.name", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for element in module.__dict__.values():
        if isinstance(element, NodeFunction.__class__):
            ALL_IMPORTED_NODE_FUNCTIONS.append(element)


NODE_FUNCTIONS_DEFINITIONS = {}
for f in ALL_IMPORTED_NODE_FUNCTIONS:
    if f.key:
        NODE_FUNCTIONS_DEFINITIONS[f.key] = f
    else:
        logger.warning(f"Function '{f.name}' has no key!")


all_keys = list(map(lambda f: f.key, NODE_FUNCTIONS_DEFINITIONS.values()))
(most_key, most_count), *rest = Counter(all_keys).most_common()
assert most_count <= 1, f"Node function key '{most_key}' exists {most_count} times!"


NODE_FUNCTIONS_CHOICES = [
    (nf.key, nf.name) for nf in NODE_FUNCTIONS_DEFINITIONS.values()
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


def run_flow(db_flowrun_id):
    db_flowrun = db_models.FlowRun.objects.get(pk=db_flowrun_id)

    # Get the backend to run the flow with
    module_name, function_name = settings.FLUXIS_RUNNER.rsplit(".", 1)
    runner_module = importlib.import_module(module_name)
    runner = getattr(runner_module, function_name)

    # -- Credentials --
    db_flow = db_flowrun.flow
    refresh_flow_oauth2credentials(db_flow)

    runner(db_flowrun)
