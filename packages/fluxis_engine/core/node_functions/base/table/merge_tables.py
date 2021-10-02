import pandas as pd

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig, PortType


class MergeTables(NodeFunction):
    name = "Merge tables"
    in_ports_conf = [
        PortConfig(
            key="table_1",
            name="Table 1",
            description="First table",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="table_2",
            name="Table 2",
            description="Second table to append to first one",
            data_type=PortType.TABLE,
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
        df1 = in_ports["table_1"]
        df2 = in_ports["table_2"]
        out_ports["table_out"] = pd.concat([df1, df2], ignore_index=True)
