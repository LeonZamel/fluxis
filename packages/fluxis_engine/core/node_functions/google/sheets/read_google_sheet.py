from io import BytesIO

import google.oauth2.credentials as google_credentials
import pandas as pd
import requests
from googleapiclient import discovery
from googleapiclient.discovery import build

from fluxis_engine.core.credentials_config import CredentialsConfig
from fluxis_engine.core.node_function import NodeFunction
from fluxis_engine.core.parameter_config import ParameterConfig, ParameterType
from fluxis_engine.core.port_config import PortConfig, PortType


class ReadGoogleSheet(NodeFunction):
    description = "Reads a Google sheet"
    explanation = "Use this connector when you want to import existing data from one of your Google sheets. \
        To use this, first connect your accounts by creating credentials and logging in to you Google account. \
            Next, find the Spreadsheet ID, by opening up the spreadsheet in Google Sheets. \
                Find the character string in the URL between the /d/ and /edit. \
                    Now enter the name of the specific sheet. You will find this in the bottom left \
                        corner when viewing your sheet."

    @staticmethod
    def suggest_spreadsheet_id(obj):
        credentials = obj.credentials
        access_token = credentials.access_token
        creds = google_credentials.Credentials(token=access_token)
        service = discovery.build("drive", "v3", credentials=creds)
        resp = (
            service.files()
            .list(
                q="mimeType='application/vnd.google-apps.spreadsheet'", spaces="drive"
            )
            .execute()
        )
        return {f["id"]: f["name"] for f in resp["files"]}

    in_ports_conf = [
        PortConfig(
            key="spreadsheet_id",
            name="Spreadsheet ID",
            description="ID of the sheet to read",
        ),
        PortConfig(
            key="sheet_name",
            name="Sheet Name",
            description="Name of the sheet to read from",
        ),
        PortConfig(
            key="range",
            name="Range",
            description="Range to read values from. Leave empty to read entire sheet",
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="table",
            name="Table",
            description="Data which was read",
            data_type=PortType.TABLE,
        )
    ]
    parameters = [
        ParameterConfig(
            key="first_line_column_names",
            name="First row are column names",
            description="Enable to treat the first row as column names",
            data_type=ParameterType.BOOLEAN,
            default_value=False,
            required=True,
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

        spreadsheet_id = in_ports["spreadsheet_id"]
        sheet_name = in_ports["sheet_name"]
        read_range = in_ports["range"]
        if read_range:
            # Read range can be empty to read the entire sheet, otherwise add the correct formatting
            read_range = f"!{read_range}"

        credentials_raw = self.credentials["token"]

        creds = google_credentials.Credentials(token=credentials_raw["access_token"])

        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(
                valueRenderOption="UNFORMATTED_VALUE",
                spreadsheetId=spreadsheet_id,
                range=f"{sheet_name}{read_range}",
            )
            .execute()
        )

        values = result.get("values", [])
        column_names = None

        if self.first_line_column_names:
            column_names = values[0]
            values = values[1:]

        df = pd.DataFrame(values, columns=column_names)
        out_ports["table"] = df

        # refresh_token, token_uri, client_id, and client_secret

        """
        resp = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{read_range}',
                            headers={'Authorization': 'Bearer ' +
                                     self.credentials['access_token']})

        
        """
