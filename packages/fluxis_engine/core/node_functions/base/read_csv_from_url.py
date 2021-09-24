import pandas as pd

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig


class ReadCSVFromURL(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="url",
            name="URL",
            description="URL to get the CSV from",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="table",
            name="Table",
            description="The read data",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        try:
            df = pd.read_csv(in_ports["url"])
            out_ports["table"] = df
        except Exception as e:
            return "Couldn't access url"
