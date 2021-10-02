from pushbullet.pushbullet import Pushbullet

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.parameter_config import ParameterConfig, ParameterType
from fluxis_engine.core.port_config import PortConfig


class SendPushbulletNotification(NodeFunction):
    name = "Send Pushbullet notification"
    in_ports_conf = [
        PortConfig(
            key="message_title",
            name="Message Title",
            description="Title of the message",
        ),
        PortConfig(
            key="message_body",
            name="Message Body",
            description="Content of the message",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="response",
            name="Response",
            description="Response object",
        )
    ]
    parameters = [
        ParameterConfig(
            key="api_key",
            name="API Key",
            description="Your Pushbullet API Key",
            data_type=ParameterType.STRING,
            default_value="",
            required=True,
        )
    ]

    def __init__(self, api_key):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.api_key = api_key

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        pb = Pushbullet(self.api_key)
        push = pb.push_note(
            str(in_ports["message_title"]), str(in_ports["message_body"])
        )
        out_ports["response"] = push
