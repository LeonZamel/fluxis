from io import BytesIO

import google.oauth2.credentials as google_credentials
import pandas as pd
import requests
from googleapiclient import discovery
from googleapiclient.discovery import build

from fluxis_engine.core.credentials_config import CredentialsConfig
from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.parameter_config import ParameterConfig, ParameterType
from fluxis_engine.core.port_config import PortConfig


class ReadGoogleAnalyticsReport(NodeFunction):
    description = "Import data from google analytics"
    explanation = "Use this connector when you want to import\
         report data from your google analytics account to automatically \
             take action upon the data."

    in_ports_conf = [
        PortConfig(
            key="view_id",
            name="View ID",
            description="View ID to get the data from",
        ),
        PortConfig(
            key="start_date",
            name="Start Date",
            description="When the report starts",
        ),
        PortConfig(
            key="end_date",
            name="End Date",
            description="When the report ends",
        ),
        PortConfig(
            key="metrics",
            name="Metrics",
            description="Range to read values from. Leave empty to read entire sheet",
        ),
        PortConfig(
            key="dimensions",
            name="Dimensions",
            description="Range to read values from. Leave empty to read entire sheet",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="table",
            name="Table",
            description="Data which was read",
        )
    ]

    credentials = CredentialsConfig(service="google_sheets")

    def __init__(self, credentials, first_line_column_names):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.credentials = credentials
        self.first_line_column_names = first_line_column_names

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        # https://developers.google.com/identity/protocols/oauth2/web-server
        # Authorization: Bearer access_token

        view_id = in_ports["view_id"]
        start_date = in_ports["start_date"]
        end_date = in_ports["end_date"]
        metrics = in_ports["metrics"]
        dimensions = in_ports["dimensions"]

        credentials_raw = self.credentials["token"]

        creds = google_credentials.Credentials(token=credentials_raw["access_token"])

        analytics = build("analyticsreporting", "v4", credentials=creds)

        response = (
            analytics.reports()
            .batchGet(
                body={
                    "reportRequests": [
                        {
                            "viewId": view_id,
                            "dateRanges": [
                                {"startDate": "7daysAgo", "endDate": "today"}
                            ],
                            "metrics": [{"expression": "ga:sessions"}],
                            "dimensions": [{"name": "ga:country"}],
                        }
                    ]
                }
            )
            .execute()
        )

        report = response.get("reports")[0]

        print(report)

        """
        resp = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{read_range}',
                            headers={'Authorization': 'Bearer ' +
                                     self.credentials['access_token']})

        
        """
