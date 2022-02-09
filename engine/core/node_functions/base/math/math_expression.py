import numpy as np
import pandas as pd
from engine.core.fluxis_exception import FluxisException
from engine.core.node_categories import NODE_CATEGORIES
from engine.core.node_function import NodeFunction
from engine.core.node_functions.base.utils import safe_eval_on_dataframe
from engine.core.port_config import PortConfig, PortSuggestion, PortType


class MathExpression(NodeFunction):
    key = "math_expression"
    name = "Math expression"
    category = NODE_CATEGORIES.TABLE
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
        df: pd.DataFrame = in_ports["table_in"]
        column_name = in_ports["column_name"]
        expression = in_ports["expression"]

        if "@" in expression:
            raise FluxisException("'@' character is not allowed in the expression.")
        try:
            res = df.eval(expression, local_dict={}, global_dict={})
        except Exception as e:
            raise FluxisException(
                f"Something went wrong evaluating the expression: {e}"
            )

        df[column_name] = res
        out_ports["table_out"] = df
