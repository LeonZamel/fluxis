from fluxis_engine.core.credentials_config import CredentialsConfig
from fluxis_engine.core.node_functions.node_function import NodeFunction
from fluxis_engine.core.port_config import PortConfig, PortType
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

import pandas as pd


class QueryPostgresql(NodeFunction):
    in_ports_conf = [
        PortConfig(
            key="query",
            name="Query",
            description="The SQL query to retrieve data",
        )
    ]
    out_ports_conf = [
        PortConfig(
            key="table_out",
            name="Table out",
            description="The retrieved data",
        )
    ]

    credentials = CredentialsConfig(service="postgresql")

    def __init__(self, credentials):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.credentials = credentials

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        url = URL(
            drivername="postgresql",
            host=self.credentials["host"],
            port=self.credentials["port"],
            database=self.credentials["database"],
            username=self.credentials["username"],
            password=self.credentials["password"],
        )

        con = create_engine(url)
        query = in_ports["query"]
        df = pd.read_sql_query(query, con=con)
        out_ports["table_out"] = df
