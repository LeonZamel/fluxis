import numpy as np
import pandas as pd
from engine.core.fluxis_exception import FluxisException
from engine.core.node_function import NodeFunction
from engine.core.port_config import PortConfig, PortSuggestion, PortType
from engine.core.node_categories import NODE_CATEGORIES


class Filter(NodeFunction):
    key = "filter"
    name = "Filter"
    category = NODE_CATEGORIES.TABLE
    in_ports_conf = [
        PortConfig(
            key="table_in",
            name="Table in",
            description="The table to filter",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="condition",
            name="Filter condition",
            description="Enter a condition. You can access the columns directly via their name.",
            suggestion=PortSuggestion(
                how="from_port", from_port="table_in", getter="column_names"
            ),
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="table_out",
            name="Table out",
            description="Filtered table",
            data_type=PortType.TABLE,
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        df: pd.DataFrame = in_ports["table_in"]
        condition = in_ports["condition"]
        if "@" in condition:
            raise FluxisException("'@' character is not allowed in the condition.")
        try:
            out_ports["table_out"] = df.query(condition, local_dict={}, global_dict={})
        except Exception as e:
            raise FluxisException(f"Something went wrong evaluating the condition: {e}")
