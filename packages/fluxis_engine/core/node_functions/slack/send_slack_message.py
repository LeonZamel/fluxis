import requests

import json

from fluxis_engine.core.node_functions.node_function import NodeFunction
from fluxis_engine.core.parameter_config import ParameterConfig
from fluxis_engine.core.port_config import PortConfig
from fluxis_engine.core.credentials_config import CredentialsConfig

API_ENDPOINT = "https://slack.com/api/chat.postMessage"


class SendSlackMessage(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="channel_id",
            name="Channel ID",
            description="ID of the channel to send the message to. Make sure to invite the bot to this channel",
        ),
        PortConfig(
            key="message",
            name="Message",
            description="Message to send",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="thread_id",
            name="Thread ID",
            description="ID of the thread that was started by this message",
        )
    ]
    credentials = CredentialsConfig(service="slack")

    def __init__(self, credentials):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.credentials = credentials

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        access_token = self.credentials["access_token"]
        resp = requests.post(
            API_ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "channel": in_ports["channel_id"],
                "text": in_ports["message"],
            },
        )

        response = json.loads(resp.content)
        if not response["ok"]:
            reason = response.get("error", "No error provided")
            if reason == "not_in_channel":
                return "Bot is not in the specified channel"
            else:
                return reason

        # Actually the timestamp, but also used as thread id
        out_ports["thread_id"] = response["ts"]
