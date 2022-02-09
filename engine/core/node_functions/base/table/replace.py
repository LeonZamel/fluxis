from engine.core.node_function import NodeFunction
from engine.core.parameter_config import ParameterConfig, ParameterType
from engine.core.port_config import PortConfig, PortType


class Replace(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="table_in",
            name="Table In",
            description="Table to replace the values in",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="on_column",
            name="Column",
            description="The column to replace the value in",
            data_type=PortType.STRING_ARRAY,
        ),
        PortConfig(
            key="to_replace",
            name="To replace",
            description="The value to replace",
            data_type=PortType.STRING_ARRAY,
        ),
        PortConfig(
            key="value",
            name="New Value",
            description="What to use as replacement",
            data_type=PortType.STRING_ARRAY,
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="table_out",
            name="Table Out",
            description="The table with replaced values",
        )
    ]
    parameters = [
        ParameterConfig(
            key="use_regex",
            name="Use Regex",
            description="If you want the replacement rules to use regex",
            data_type=ParameterType.BOOLEAN,
            default_value=False,
        )
    ]

    def __init__(self, use_regex):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.use_regex = use_regex

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        df = in_ports["table_in"]
        column = in_ports["on_column"]
        to_replace = in_ports["to_replace"]

        df_out = df.replace(regex=self.use_regex)

        out_ports["table_out"] = df_out
