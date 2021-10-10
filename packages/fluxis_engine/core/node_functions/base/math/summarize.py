import numpy as np
import pandas as pd
from fluxis_engine.core.node_categories import NODE_CATEGORIES
from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.parameter_config import ParameterConfig, ParameterType
from fluxis_engine.core.port_config import PortConfig, PortSuggestion, PortType


class Summarize(NodeFunction):
    key = "summarize"
    name = "Summarize"
    category = NODE_CATEGORIES.TABLE
    in_ports_conf = [
        PortConfig(
            key="table_in",
            name="Table in",
            description="The Table to summarize on",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="group_by",
            name="Group By",
            description="The columns to group by",
            data_type=PortType.STRING_ARRAY,
            suggestion=PortSuggestion(
                how="from_port", from_port="table_in", getter="column_names"
            ),
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="table_out",
            name="Table out",
            description="The summarized data",
        )
    ]
    parameters = [
        ParameterConfig(
            key="summarize_function",
            name="Summarize function",
            description="How to summarize the groups",
            data_type=ParameterType.STRING,
            required=True,
            default_value="Count",
            choices=[
                "Count",
                "Count Unique",
                "Sum",
                "Mean",
                "Median",
                "First",
                "Last",
                "Max",
                "Min",
            ],
        )
    ]

    def __init__(self, summarize_function):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.summarize_function = summarize_function

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        df = in_ports["table_in"]
        res = None
        by = in_ports["group_by"]
        # If no column to group on is given, don't group at all
        grouped = df.groupby(by if by else lambda _: True)
        if self.summarize_function == "Count":
            res = grouped.count()
        elif self.summarize_function == "Count Unique":
            res = grouped.nunique()
        elif self.summarize_function == "Sum":
            res = grouped.sum()
        elif self.summarize_function == "Mean":
            res = grouped.mean()
        elif self.summarize_function == "Median":
            res = grouped.median()
        elif self.summarize_function == "First":
            res = grouped.first()
        elif self.summarize_function == "Last":
            res = grouped.last()
        elif self.summarize_function == "Max":
            res = grouped.max()
        elif self.summarize_function == "Min":
            res = grouped.min()
        else:
            return f"Unknown summarize function: '{self.summarize_function}'"
        # If there wasn't any column to group by we now have a new column as index which we would like to drop
        drop_index = not bool(by)
        out_ports["table_out"] = res.reset_index(drop=drop_index)
