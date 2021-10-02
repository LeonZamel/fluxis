from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig, PortType


class AddColumn(NodeFunction):
    name = "Add column"
    in_ports_conf = [
        PortConfig(
            key="table_in",
            name="Table in",
            description="The table to add the column to",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="column_name",
            name="Column name",
            description="Name of the new column",
        ),
        PortConfig(
            key="default_val",
            name="Default value",
            description="Value to fill the new column with",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="table_out",
            name="Table out",
            description="The table with the new column",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        df = in_ports["table_in"]
        df[in_ports["column_name"]] = in_ports["default_val"]
        out_ports["table_out"] = df
