import pandas as pd

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig, PortType


class Predict(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="features",
            name="Features",
            description="Features to predict on",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="model",
            name="Model",
            description="Model to use for prediction",
            data_type=PortType.ML_MODEL,
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="prediction",
            name="Prediction",
            description="Prediction for the data",
            data_type=PortType.TABLE,
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        features = in_ports["features"]
        classifier = in_ports["model"]
        res = classifier.predict(features)
        out_ports["prediction"] = res
