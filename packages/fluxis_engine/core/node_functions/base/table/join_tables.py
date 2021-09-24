import pandas as pd

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig, PortType


class JoinTables(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="table_left",
            name="Table Left",
            description="First table to use for joining",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="table_right",
            name="Table Right",
            description="Second table to use for joining",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="column",
            name="Column",
            description="The column to join on",
            data_type=PortType.STRING,
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="table_out",
            name="Merged Tables",
            description="The merged tables",
            data_type=PortType.TABLE,
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        df1 = in_ports["table_left"]
        df2 = in_ports["table_right"]
        column = in_ports["column"]
        out_ports["table_out"] = df1.merge(df2, on=column)
