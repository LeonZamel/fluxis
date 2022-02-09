from sklearn.tree import DecisionTreeRegressor as dtr

from engine.core.node_function import NodeFunction
from engine.core.port_config import PortConfig, PortType


class DecisionTreeRegressor(NodeFunction):
    name = "Decision Tree Regressor"
    in_ports_conf = [
        PortConfig(
            key="features",
            name="Features",
            description="Features to base the learning upon",
            data_type=PortType.TABLE,
        ),
        PortConfig(
            key="regression_labels",
            name="Regression labels",
            description="Labels to base the learning upon",
            data_type=PortType.TABLE,
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="regressor",
            name="Regressor",
            description="The trained regressor",
            data_type=PortType.ML_MODEL,
        )
    ]

    def __init__(self):
        super().__init__(self.in_ports_conf, self.out_ports_conf)

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        X = in_ports["features"]
        y = in_ports["regression_labels"]
        clf = dtr(random_state=0)
        clf.fit(X, y)
        out_ports["regressor"] = clf
