from fluxis_engine.core.node_functions.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig


class TextTemplate(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="text_in",
            name="Template Text",
            description="The text you want to use as template",
        ),
        PortConfig(
            key="variables",
            name="Variables",
            description="Variables which should be inserted into the template. Reference with {variable_name}",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="text_out",
            name="Text",
            description="The resulting text",
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        template_text = in_ports["text_in"]
        variables = in_ports["variables"]
        result = template_text.format(**variables)
        out_ports["text_out"] = result
