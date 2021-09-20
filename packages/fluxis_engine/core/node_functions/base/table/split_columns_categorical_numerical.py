import pandas as pd

from fluxis_engine.core.node_functions.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig


class SplitColumnsCategoricalNumerical(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="table_in",
            name="Table in",
            description="Table to rename the columns of",
        ),
        PortConfig(
            key="threshold",
            name="Threshold",
            description="Up to how many unique values to still be considered categorical (inclusive)",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="columns_categorical",
            name="Columns Categorical",
            description="The column names of Categorical",
        ),
        PortConfig(
            key="columns_numerical",
            name="Columns Categorical",
            description="The column names of Categorical",
        ),
        PortConfig(
            key="columns_unassignable",
            name="Columns unassignable",
            description="Columns that aren't numbers but have too many distinct values",
        ),
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        pass
        """
        cat_cols = df.nunique()[df.nunique() <=
                                in_ports['threshold']].keys().tolist()
        num_cols = [x for x in df.columns if x not in cat_cols +
                    target_col + Id_col]
        df = in_ports['table_in']
        rename_map = in_ports['rename_map']
        df = df.rename(rename_map, axis='columns')
        out_ports['table_out'] = df
        """
