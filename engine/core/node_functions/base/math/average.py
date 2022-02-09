import numpy as np
import pandas as pd

from engine.core.node_function import NodeFunction
from engine.core.port_config import PortConfig


class Average(NodeFunction):
    name = "Average"
    in_ports_conf = [
        PortConfig(
            key="values",
            name="Values",
            description="List of values to take the average of",
        )
    ]
    out_ports_conf = [
        PortConfig(
            key="average",
            name="Average",
            description="Average of input numbers",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        orig_data = in_ports["values"]
        numeric_array = pd.to_numeric(orig_data, errors="coerce")
        na_indices = numeric_array.isna()
        na_vals = orig_data[na_indices]
        if na_vals.empty:
            out_ports["average"] = np.average(numeric_array)
        else:
            return "Not all values are numeric: " + str(na_vals.values)
