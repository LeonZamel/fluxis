import pandas as pd

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig


class RenameColumns(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="table_in",
            name="Table in",
            description="Table to rename the columns of",
        ),
        PortConfig(
            key="rename_map",
            name="Rename Map",
            description="How to rename the columns. Non existing names will be ignored",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="table_out",
            name="Tables out",
            description="The new table with renamed columns",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        df = in_ports["table_in"]
        rename_map = in_ports["rename_map"]
        df = df.rename(rename_map, axis="columns")
        out_ports["table_out"] = df
