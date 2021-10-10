from io import StringIO
import pandas as pd

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig
from fluxis_engine.core.node_categories import NODE_CATEGORIES


class ParseCSV(NodeFunction):
    key = "parse_csv"
    name = "Parse CSV"
    category = NODE_CATEGORIES.DATA_IN
    in_ports_conf = [
        PortConfig(
            key="text",
            name="Text",
            description="The text to parse",
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
        data = StringIO(in_ports["text"])
        df = pd.read_csv(data)
        out_ports["table"] = df
