from enum import Enum

from fluxis_engine.core.node_functions.base.filter import Filter
from fluxis_engine.core.node_functions.base.http_request import HTTPRequest
from fluxis_engine.core.node_functions.base.if_else import IfElse
from fluxis_engine.core.node_functions.base.is_nan import IsNaN
from fluxis_engine.core.node_functions.base.length import Length
from fluxis_engine.core.node_functions.base.logical_not import LogicalNot
from fluxis_engine.core.node_functions.base.math.average import Average
from fluxis_engine.core.node_functions.base.math.math_expression import MathExpression
from fluxis_engine.core.node_functions.base.math.sum import Sum
from fluxis_engine.core.node_functions.base.math.summarize import Summarize
from fluxis_engine.core.node_functions.base.object.create_object import CreateObject
from fluxis_engine.core.node_functions.base.object.get_object_keys import GetObjectKeys
from fluxis_engine.core.node_functions.base.object.get_object_value_by_key import (
    GetObjectValueByKey,
)
from fluxis_engine.core.node_functions.base.object.parse_json import ParseJSON
from fluxis_engine.core.node_functions.base.object.set_object_value_by_key import (
    SetObjectValueByKey,
)
from fluxis_engine.core.node_functions.base.read_csv_from_url import ReadCSVFromURL
from fluxis_engine.core.node_functions.base.select_columns import SelectColumns
from fluxis_engine.core.node_functions.base.table.add_column import AddColumn
from fluxis_engine.core.node_functions.base.table.join_tables import JoinTables
from fluxis_engine.core.node_functions.base.table.merge_tables import MergeTables
from fluxis_engine.core.node_functions.base.table.rename_columns import RenameColumns
from fluxis_engine.core.node_functions.base.table.sort import Sort
from fluxis_engine.core.node_functions.base.table.to_number import ToNumber
from fluxis_engine.core.node_functions.base.text.text_template import TextTemplate
from fluxis_engine.core.node_functions.base.trigger.manual_trigger import ManualTrigger
from fluxis_engine.core.node_functions.google.analytics.read_google_analytics_report import (
    ReadGoogleAnalyticsReport,
)
from fluxis_engine.core.node_functions.google.sheets.read_google_sheet import (
    ReadGoogleSheet,
)
from fluxis_engine.core.node_functions.google.sheets.write_google_sheet import (
    WriteGoogleSheet,
)
from fluxis_engine.core.node_functions.intelligence.machine_learning.decision_tree_regressor import (
    DecisionTreeRegressor,
)
from fluxis_engine.core.node_functions.intelligence.machine_learning.support_vector_machine import (
    SupportVectorMachine,
)
from fluxis_engine.core.node_functions.intelligence.predict import Predict
from fluxis_engine.core.node_functions.pushbullet.send_pushbullet_notification import (
    SendPushbulletNotification,
)
from fluxis_engine.core.node_functions.slack.send_slack_message import SendSlackMessage
from fluxis_engine.core.node_functions.sql.query_postgresql import QueryPostgresql

NODE_FUNCTIONS = [
    SelectColumns,
    RenameColumns,
    AddColumn,
    MergeTables,
    JoinTables,
    Filter,
    Sort,
    ToNumber,
    MathExpression,
    Summarize,
    IsNaN,
    LogicalNot,
    TextTemplate,
    SupportVectorMachine,
    DecisionTreeRegressor,
    Predict,
    HTTPRequest,
    ReadCSVFromURL,
    ReadGoogleSheet,
    QueryPostgresql,
    ReadGoogleAnalyticsReport,
    SendPushbulletNotification,
    SendSlackMessage,
    WriteGoogleSheet,
]
