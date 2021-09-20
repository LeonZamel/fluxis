import numpy as np
import pandas as pd

from fluxis_engine.core.node_functions.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig, PortSuggestion, PortType

from fluxis_engine.core.parameter_config import ParameterConfig, ParameterType


class ToNumber(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="table_in",
            name="Table in",
            description="The Table to summarize on",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="column_names",
            name="Columns",
            description="The columns to make numeric",
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
            description="The modified table",
        )
    ]
    parameters = [
        ParameterConfig(
            key="remove_characters",
            name="Remove Characters",
            description="If text characters (all characters except for digits and decimal points) should be removed first.",
            data_type=ParameterType.BOOLEAN,
            required=True,
            default_value=False,
        )
    ]

    def __init__(self, remove_characters):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.remove_characters = remove_characters

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        df = in_ports["table_in"].copy()
        columns = in_ports["column_names"]
        for col_name in columns:
            col = df[col_name]
            if self.remove_characters:
                col = col.replace(r"\D+", "", regex=True)
            df[col_name] = pd.to_numeric(col, errors="coerce")

        out_ports["table_out"] = df
