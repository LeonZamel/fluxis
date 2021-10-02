import requests

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig


class HTTPRequest(NodeFunction):
    name = "Http Request"
    in_ports_conf = [
        PortConfig(
            key="url",
            name="URL",
            description="The URL to access",
        ),
        PortConfig(
            key="parameters",
            name="Parameters",
            description="Parameters to pass in the url",
        ),
        PortConfig(
            key="data",
            name="Data",
            description="Data to pass in the request",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="response",
            name="Response",
            description="Response",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        url = in_ports["url"]
        parameters = in_ports["parameters"]
        data = in_ports["data"]

        response = requests.get(url, params=parameters).json()

        response = requests.post(url, data=data).json()

        out_ports["response"] = response
