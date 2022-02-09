import requests
from engine.core.node_categories import NODE_CATEGORIES
from engine.core.node_function import NodeFunction
from engine.core.port_config import PortConfig


class HTTPRequest(NodeFunction):
    key = "http_get_request"
    name = "Http Request"
    category = NODE_CATEGORIES.DATA_IN
    in_ports_conf = [
        PortConfig(
            key="url",
            name="URL",
            description="The URL to access",
        ),
        PortConfig(
            key="parameters",
            name="Parameters/Data",
            description="Parameters/Data to pass in the request either as get parameters or additional data",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="response",
            name="Response",
            description="Response",
        ),
        PortConfig(
            key="data",
            name="Data",
            description="Response Data",
        ),
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        url = in_ports["url"]
        parameters = in_ports["parameters"]
        response = requests.get(url, params=parameters)
        out_ports["response"] = response
        out_ports["data"] = response.text
