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


class NODE_CATEGORIES(Enum):
    # TRIGGER = "Trigger"
    # CONTROL_FLOW = "Control Flow"
    TABLE = "Table"
    # OBJECT = "Object"
    # ARRAY = "Array"
    MATH = "Math"
    # LOGIC = "Logic"
    TEXT = "Text"
    # INTELLIGENCE = "Intelligence"
    DATA_IN = "Data sources"
    DATA_OUT = "Data destinations"


NODE_FUNCTIONS = {
    # TRIGGER
    # "manual_trigger": (ManualTrigger, "Manual Trigger", NODE_CATEGORIES.TRIGGER),
    # CONTROL_FLOW
    # "if_else": (IfElse, "If Else condition", NODE_CATEGORIES.CONTROL_FLOW),
    # "gate": (GateFunction, "Gate", NODE_CATEGORIES.CONTROL_FLOW),
    # "constant_value": (ConstantValueFunction, "Constant value", NODE_CATEGORIES.CONTROL_FLOW),
    # TABLE
    "select_columns": (SelectColumns, "Select columns", NODE_CATEGORIES.TABLE),
    # "rename_colums": (RenameColumns, "Rename columns", NODE_CATEGORIES.TABLE),
    "add_column": (AddColumn, "Add column", NODE_CATEGORIES.TABLE),
    "merge_tables": (MergeTables, "Merge tables", NODE_CATEGORIES.TABLE),
    "join_tables": (JoinTables, "Join tables", NODE_CATEGORIES.TABLE),
    "filter": (Filter, "Filter", NODE_CATEGORIES.TABLE),
    "sort": (Sort, "Sort", NODE_CATEGORIES.TABLE),
    "to_number": (ToNumber, "To Number", NODE_CATEGORIES.TABLE),
    # "replace": (Replace, "Replace", NODE_CATEGORIES.TABLE),
    # OBJECT
    # "create_object": (CreateObject, "Create object", NODE_CATEGORIES.OBJECT),
    # "object_set_by_key": (SetObjectValueByKey, "Set object value by key", NODE_CATEGORIES.OBJECT),
    # "object_get_by_key": (GetObjectValueByKey, "Get object value by key", NODE_CATEGORIES.OBJECT),
    # "object_get_keys": (GetObjectKeys, "Get object keys", NODE_CATEGORIES.OBJECT),
    # "parse_json": (ParseJSON, "Parse JSON", NODE_CATEGORIES.OBJECT),
    # ARRAY
    # "length": (Length, "Length of iterable", NODE_CATEGORIES.ARRAY),
    # "create_array": (CreateArrayFunction, "Create new array", NODE_CATEGORIES.ARRAY),
    # "append_to_array": (AppendToArrayFunction, "Append to array", NODE_CATEGORIES.ARRAY),
    # "merge_arrays": (MergeArraysFunction, "Merge arrays", NODE_CATEGORIES.ARRAY),
    # "set_array_value_at_index": (SetArrayValueAtIndexFunction, "Set array value at index", NODE_CATEGORIES.ARRAY),
    # "get_array_value_at_index": (GetArrayValueAtIndexFunction, "Get array value at index", NODE_CATEGORIES.ARRAY),
    # MATH
    "math_expression": (
        MathExpression,
        "Mathematical expression",
        NODE_CATEGORIES.MATH,
    ),
    "summarize": (Summarize, "Summarize", NODE_CATEGORIES.MATH),
    # "average": (Average, "Average", NODE_CATEGORIES.MATH),
    # "sum": (Sum, "Sum", NODE_CATEGORIES.MATH),
    "is_nan": (IsNaN, "Is NaN", NODE_CATEGORIES.MATH),
    # LOGIC
    # "logical_not": (LogicalNot, "Logical not", NODE_CATEGORIES.LOGIC),
    # TEXT
    "text_template": (TextTemplate, "Text template", NODE_CATEGORIES.TEXT),
    # INTELLIGENCE
    # "support_vector_machine": (SupportVectorMachine, "Support Vector Machine", NODE_CATEGORIES.INTELLIGENCE),
    # "decision_tree_regressor": (DecisionTreeRegressor, "Decision Tree Regressor", NODE_CATEGORIES.INTELLIGENCE),
    # "predict": (Predict, "Predict", NODE_CATEGORIES.INTELLIGENCE),
    # DATA_IN
    "http_request": (HTTPRequest, "HTTP Request", NODE_CATEGORIES.DATA_IN),
    "read_csv_from_url": (ReadCSVFromURL, "Read CSV from URL", NODE_CATEGORIES.DATA_IN),
    "read_google_sheet": (
        ReadGoogleSheet,
        "Read Google Sheet",
        NODE_CATEGORIES.DATA_IN,
    ),
    "query_postgresql": (
        QueryPostgresql,
        "Query Postrgresql Database",
        NODE_CATEGORIES.DATA_IN,
    ),
    "import_google_analytics": (
        ReadGoogleAnalyticsReport,
        "Import Google Analytics data",
        NODE_CATEGORIES.DATA_IN,
    ),
    # DATA_OUT
    "send_pushbullet_notification": (
        SendPushbulletNotification,
        "Send Pushbullet notification",
        NODE_CATEGORIES.DATA_OUT,
    ),
    "send_slack_message": (
        SendSlackMessage,
        "Send message to slack",
        NODE_CATEGORIES.DATA_OUT,
    ),
    "write_google_sheet": (
        WriteGoogleSheet,
        "Write to Google Sheet",
        NODE_CATEGORIES.DATA_OUT,
    ),
}
