import numpy as np

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig, PortType, PortSuggestion

from .utils import safe_eval_on_dataframe


class Filter(NodeFunction):
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
        df = in_ports["table_in"]
        condition = in_ports["condition"]
        bools = safe_eval_on_dataframe(condition, df)
        try:
            if bools.dtype.name == "bool":
                out_ports["table_out"] = df[bools]
            else:
                return "Condition doesn't evaluate to True or False values"
        except Exception as e:
            return "Something went wrong evaluating the condition"
