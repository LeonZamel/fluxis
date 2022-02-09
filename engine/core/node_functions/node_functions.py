from enum import Enum

from engine.core.node_functions.base.filter import Filter
from engine.core.node_functions.base.http_request import HTTPRequest
from engine.core.node_functions.base.if_else import IfElse
from engine.core.node_functions.base.is_nan import IsNaN
from engine.core.node_functions.base.length import Length
from engine.core.node_functions.base.logical_not import LogicalNot
from engine.core.node_functions.base.math.average import Average
from engine.core.node_functions.base.math.math_expression import MathExpression
from engine.core.node_functions.base.math.sum import Sum
from engine.core.node_functions.base.math.summarize import Summarize
from engine.core.node_functions.base.object.create_object import CreateObject
from engine.core.node_functions.base.object.get_object_keys import GetObjectKeys
from engine.core.node_functions.base.object.get_object_value_by_key import (
    GetObjectValueByKey,
)
from engine.core.node_functions.base.object.parse_json import ParseJSON
from engine.core.node_functions.base.object.set_object_value_by_key import (
    SetObjectValueByKey,
)
from engine.core.node_functions.base.parse_csv import ParseCSV
from engine.core.node_functions.base.select_columns import SelectColumns
from engine.core.node_functions.base.table.add_column import AddColumn
from engine.core.node_functions.base.table.join_tables import JoinTables
from engine.core.node_functions.base.table.merge_tables import MergeTables
from engine.core.node_functions.base.table.rename_columns import RenameColumns
from engine.core.node_functions.base.table.sort import Sort
from engine.core.node_functions.base.table.to_number import ToNumber
from engine.core.node_functions.base.text.text_template import TextTemplate
from engine.core.node_functions.base.trigger.manual_trigger import ManualTrigger
from engine.core.node_functions.google.analytics.read_google_analytics_report import (
    ReadGoogleAnalyticsReport,
)
from engine.core.node_functions.google.sheets.read_google_sheet import (
    ReadGoogleSheet,
)
from engine.core.node_functions.google.sheets.write_google_sheet import (
    WriteGoogleSheet,
)
from engine.core.node_functions.intelligence.machine_learning.decision_tree_regressor import (
    DecisionTreeRegressor,
)
from engine.core.node_functions.intelligence.machine_learning.support_vector_machine import (
    SupportVectorMachine,
)
from engine.core.node_functions.intelligence.predict import Predict
from engine.core.node_functions.pushbullet.send_pushbullet_notification import (
    SendPushbulletNotification,
)
from engine.core.node_functions.slack.send_slack_message import SendSlackMessage
from engine.core.node_functions.sql.query_postgresql import QueryPostgresql

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
    ParseCSV,
    ReadGoogleSheet,
    QueryPostgresql,
    ReadGoogleAnalyticsReport,
    SendPushbulletNotification,
    SendSlackMessage,
    WriteGoogleSheet,
]
