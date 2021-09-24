import pandas as pd

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig


class WriteExcel(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="table",
            name="Table",
            description="Table to write to the file",
        ),
        PortConfig(
            key="file_name",
            name="File name",
            description="Name of the written file",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="excel_file",
            name="Excel File",
            description="The created excel file",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        df = in_ports["table"]
        out_ports["excel_file"] = df.to_excel(
            in_ports["file_name"] + ".xlsx", index=False
        )
