import pandas as pd
from sklearn import svm

from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig, PortType


class SupportVectorMachine(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="features",
            name="Features",
            description="Features to base the learning upon",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="class_labels",
            name="Class labels",
            description="Labels to base the learning upon",
            data_type=PortType.TABLE,
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="classifier",
            name="Classifier",
            description="The trained classifier",
            data_type=PortType.ML_MODEL,
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        X = in_ports["features"]
        y = in_ports["class_labels"]
        clf = svm.SVC()
        clf.fit(X, y)
        out_ports["classifier"] = clf
