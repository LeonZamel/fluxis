from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.parameter_config import ParameterConfig, ParameterType
from fluxis_engine.core.port_config import PortConfig, PortType, PortSuggestion


class Sort(NodeFunction):
    name = "Sort"
    in_ports_conf = [
        PortConfig(
            key="table_in",
            name="Table In",
            description="Table to sort",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="column_names",
            name="Column names",
            description="The columns to sort by",
            data_type=PortType.STRING_ARRAY,
            suggestion=PortSuggestion(
                how="from_port", from_port="table_in", getter="column_names"
            ),
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="table_out",
            name="Table Out",
            description="The sorted table",
        )
    ]
    parameters = [
        ParameterConfig(
            key="ascending",
            name="Ascending",
            description="If the values should be sorted in ascending order instead of descending",
            data_type=ParameterType.BOOLEAN,
            default_value=False,
        )
    ]

    def __init__(self, ascending):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.ascending = ascending

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        names = in_ports["column_names"]
        df = in_ports["table_in"]
        new_df = df.sort_values(names, ascending=self.ascending)
        out_ports["table_out"] = new_df
