import numpy as np
import pandas as pd

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig


class Sum(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="values",
            name="Values",
            description="List of values to sum up",
        )
    ]
    out_ports_conf = [
        PortConfig(
            key="sum",
            name="Sum",
            description="Sum of input numbers",
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
            out_ports["sum"] = np.sum(numeric_array)
        else:
            return "Not all values are numeric: " + str(na_vals.values)
