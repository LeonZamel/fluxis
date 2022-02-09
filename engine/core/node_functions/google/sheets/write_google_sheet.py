from io import BytesIO

import google.oauth2.credentials as google_credentials
import pandas as pd
import requests
from googleapiclient import discovery
from googleapiclient.discovery import build

import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

from engine.core.credentials_config import CredentialsConfig
from engine.core.node_function import NodeFunction
from engine.core.parameter_config import ParameterConfig, ParameterType
from engine.core.port_config import PortConfig, PortType
from engine.core.node_categories import NODE_CATEGORIES


class WriteGoogleSheet(NodeFunction):
    name = "Write Google sheet"
    key = "write_google_sheet"
    category = NODE_CATEGORIES.DATA_OUT
    description = "Writes data to a new Google sheet"
    explanation = "Use this connector when you want to create a new Google Sheet with data from your flow."

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
            key="spreadsheet_name",
            name="Spreadsheet Name",
            description="Name of the Spreadsheet to create",
        ),
        PortConfig(
            key="sheet_name",
            name="Sheet Name",
            description="Name of the sheet",
        ),
        PortConfig(
            key="table_in",
            name="Table",
            description="Table data to write to the newly created sheet",
            data_type=PortType.TABLE,
        ),
    ]
    out_ports_conf = [
        PortConfig(
            key="spreadsheet_id",
            name="Spreadsheet ID",
            description="ID of the newly created spreadsheet",
        )
    ]
    parameters = [
        ParameterConfig(
            key="write_column_names",
            name="Write column names",
            description="Enable if you want the column names to be written",
            data_type=ParameterType.BOOLEAN,
            default_value=True,
            required=True,
        )
    ]

    credentials = CredentialsConfig(service="google_sheets")

    def __init__(self, credentials, write_column_names):
        super().__init__(self.in_ports_conf, self.out_ports_conf)
        self.credentials = credentials
        self.write_column_names = write_column_names

    def run(
        self, in_ports: dict, out_ports: dict, in_ports_ref: dict, out_ports_ref: dict
    ):
        # https://developers.google.com/identity/protocols/oauth2/web-server
        # Authorization: Bearer access_token

        spreadsheet_name = in_ports["spreadsheet_name"]
        sheet_name = in_ports["sheet_name"]
        table = in_ports["table_in"]

        credentials_raw = self.credentials["token"]

        creds = google_credentials.Credentials(token=credentials_raw["access_token"])

        api_client = gspread.authorize(creds)

        sh = api_client.create(spreadsheet_name)
        worksheet = sh.sheet1
        worksheet.update_title(sheet_name)

        worksheet.update([table.columns.values.tolist()] + table.values.tolist())
        # set_with_dataframe(worksheet, table) # Gives weird formatting errors

        out_ports["spreadsheet_id"] = sh.id

        """
        service = build('sheets', 'v4', credentials=creds)
        """
        """
        if self.write_column_names:
            pass
        """

        # Call the Sheets API
        """"
        sheets_api = service.spreadsheets()
        result = sheets_api.create(body=spreadsheet_body).execute()
        """
        """
        values = result.get('values', [])
        column_names = None

        df = pd.DataFrame(values, columns=column_names)
        out_ports['table'] = df
        """

        # refresh_token, token_uri, client_id, and client_secret

        """
        resp = requests.get(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{read_range}',
                            headers={'Authorization': 'Bearer ' +
                                     self.credentials['access_token']})

        
        """
