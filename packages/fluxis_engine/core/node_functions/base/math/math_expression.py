import numpy as np
import pandas as pd

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig, PortType, PortSuggestion

from fluxis_engine.core.node_functions.base.utils import safe_eval_on_dataframe


class MathExpression(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="table_in",
            name="Table",
            description="Table on which to add the column",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="column_name",
            name="Column Name",
            description="Name for the newly created column",
        ),
        PortConfig(
            key="expression",
            name="Expression",
            description="The expression to evaluate",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="table_out",
            name="Result",
            description="The table with the expression evaluated as a new column",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        df = in_ports["table_in"]
        column_name = in_ports["column_name"]
        val = safe_eval_on_dataframe(in_ports["expression"], df)
        df[column_name] = val
        out_ports["table_out"] = df
