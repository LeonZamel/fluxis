from fluxis_engine.core.node_functions.node_function import NodeFunction
from fluxis_engine.core.parameter_config import ParameterConfig, ParameterType
from fluxis_engine.core.port_config import PortConfig, PortType


class SelectColumns(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="table_in",
            name="Table In",
            description="Table to select the columns from",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="column_names",
            name="Column names",
            description="The columns to select from the table",
            data_type=PortType.STRING_ARRAY,
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="table_out",
            name="Table Out",
            description="The selected columns",
        )
    ]
    parameters = [
        ParameterConfig(
            key="remove_selected",
            name="Remove selected",
            description="If you want the selected columns to be removed instead of kept",
            data_type=ParameterType.BOOLEAN,
            default_value=False,
        )
    ]

    def __init__(self, remove_selected):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.remove_selected = remove_selected

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        names = in_ports["column_names"]
        df = in_ports["table_in"]
        try:
            if self.remove_selected:
                out_ports["table_out"] = df.drop(names, axis=1)
            else:
                # We want to preserve the order of the df, so we drop all the ones which aren't selected
                out_ports["table_out"] = df.drop(
                    [name for name in df.columns if name not in names], axis=1
                )
        except KeyError as e:
            return e.args[0]
