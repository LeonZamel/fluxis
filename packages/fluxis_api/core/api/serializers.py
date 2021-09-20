from enum import Enum
from itertools import chain

import numpy as np
import pandas as pd

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.fields import CurrentUserDefault, DateTimeField, TimeField

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from core.adapter import (
    NODE_FUNCTIONS_DEFINITIONS,
    get_function,
    refresh_flow_oauth2credentials,
)
from core.data_store import read_output_for_noderun
from core.models import (
    BaseInPort,
    ConstantValue,
    Edge,
    Flow,
    FlowConfig,
    FlowRun,
    FlowRunSchedule,
    HttpEndpointTrigger,
    InPort,
    Node,
    NodeRun,
    NodeRunExtraOutput,
    OutPort,
    Parameter,
    Port,
    TimerTrigger,
    Trigger,
    TriggerInPort,
)
from fluxis_engine.core.parameter_config import ParameterType
from authentication.models import OAuth2Credentials
from authentication.serializers import (
    OAuth2CredentialsSerializer,
    CredentialsSerializer,
)

import json
import datetime


"""
class BaseInPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseInPort
        fields = ('key', )
"""
"""
class InPortCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InPort
        fields = ('id', 'node', 'key')
        read_only_fields = ('node',)


class OutPortCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutPort
        fields = ('id', 'node', 'key')
        read_only_fields = ('node',)
"""


def create_trigger_port(node):
    if not has_trigger_port(node):
        TriggerInPort.objects.create(node=node, key="trigger")


def must_have_trigger_port(node):
    if NODE_FUNCTIONS_DEFINITIONS[node.function]["is_trigger_node"]:
        return False
    in_ports_of_node = InPort.objects.filter(node__exact=node)
    return len(in_ports_of_node) == 0 or all(
        hasattr(port_instance, "constant_value") for port_instance in in_ports_of_node
    )


def has_trigger_port(node):
    return hasattr(node, "trigger_port")


def auto_create_trigger_port(node):
    if must_have_trigger_port(node):
        create_trigger_port(node)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "flows")


class ConstantValueSerializerInPort(serializers.ModelSerializer):
    # We don't need to send the port when the value is sent from within a port
    class Meta:
        model = ConstantValue
        fields = (
            "data_type",
            "value",
        )


class ConstantValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstantValue
        fields = ("port", "data_type", "value")


class BaseInPortMasterSerializer(serializers.Serializer):
    # This is needed to automatically parse a port and determine its actual type
    def to_representation(self, value):
        # Can't this be done nicer?
        if InPort.objects.filter(id__exact=value.id).exists():
            return InPortSerializer(
                instance=InPort.objects.get(id__exact=value.id)
            ).data
        elif TriggerInPort.objects.filter(id__exact=value.id).exists():
            return TriggerInPortSerializer(
                instance=TriggerInPort.objects.get(id__exact=value.id)
            ).data
        raise Exception("Unexpected type of port object")

    def to_internal_value(self, data):
        # Can't this be done nicer?
        node = data.get("node")
        key = data.get("key")
        if not node:
            raise serializers.ValidationError({"node": "This field is required."})
        if not key:
            raise serializers.ValidationError({"key": "This field is required."})
        if key == "trigger":
            return TriggerInPortSerializer().to_internal_value(data)
        else:
            return InPortSerializer().to_internal_value(data)


class InPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = InPort
        fields = ("node", "key")


class TriggerInPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriggerInPort
        fields = ("node", "key")
        extra_kwargs = {
            "node": {"validators": []},
        }


class TriggerInPortSerializerInNode(serializers.ModelSerializer):
    # We don't need to send the node when the port is sent from within a node
    class Meta:
        model = TriggerInPort
        fields = ("key",)


class InPortSerializerInNode(serializers.ModelSerializer):
    constant_value = ConstantValueSerializerInPort(required=False, many=False)
    # We don't need to send the node when the port is sent from within a node

    class Meta:
        model = InPort
        fields = ("key", "constant_value")


class OutPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutPort
        fields = ("node", "key")


class OutPortSerializerInNode(serializers.ModelSerializer):
    class Meta:
        model = OutPort
        fields = ("key",)


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ("key", "data_type", "value")

    """
    def to_representation(self, obj):

        Translate object to internal data representation

        Override to allow polymorphism

        if hasattr(obj, 'data_type'):
            data_type_str = obj.data_type
            if isinstance(data_type_str, Enum):
                data_type_str = data_type_str.value
        else:
            raise ValueError(
                'Cannot get data_type of Parameter', )

        try:
            serializer = self.get_serializer_map()[data_type_str]
        except KeyError:
            raise ValueError(
                'Serializer for "{}" does not exist'.format(data_type_str), )

        data = serializer(obj, context=self.context).to_representation(obj)
        data['data_type'] = data_type_str
        return data
    """


"""
class NodeSerializer(serializers.ModelSerializer):
    in_ports = InPortSerializerInNode(many=True)
    out_ports = OutPortSerializerInNode(many=True)
    parameters = ParameterSerializer(many=True)
    trigger_port = TriggerInPortSerializerInNode(many=False)

    class Meta:
        model = Node
        fields = ('id', 'flow', 'name', 'x', 'y',
                  'function', 'in_ports', 'out_ports', 'parameters', 'trigger_port')
        read_only_fields = ('in_ports', 'out_ports', 'parameters')
"""


class NodeSerializer(serializers.ModelSerializer):
    # For node serialized within in flow
    in_ports = InPortSerializerInNode(many=True)
    out_ports = OutPortSerializerInNode(many=True)
    parameters = ParameterSerializer(many=True)
    trigger_port = TriggerInPortSerializerInNode(many=False)
    credentials = CredentialsSerializer()

    class Meta:
        model = Node
        fields = (
            "id",
            "name",
            "x",
            "y",
            "function",
            "in_ports",
            "out_ports",
            "parameters",
            "trigger_port",
            "credentials",
        )
        read_only_fields = ("id", "in_ports", "out_ports", "parameters")


class NodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        # Flow gets set automatically in view
        fields = ("id", "name", "x", "y", "function")
        read_only_fields = ("id",)

    def create(self, validated_data):
        function = validated_data["function"]
        # We make this transaction atomic, if anything fails we don't have a broken node in our db
        with transaction.atomic():
            node = Node.objects.create(**validated_data)
            self.create_parameters(node, function)
            self.create_ports(node, function)
            # auto_create_trigger_port(node)
            return node

    def create_parameters(self, node, function):
        # We create the parameters with an empty value. The value can then be PATCHed by the client later
        parameters = NODE_FUNCTIONS_DEFINITIONS[function]["parameters"]
        for parameter in parameters:
            Parameter.objects.create(
                value="",
                node=node,
                key=parameter["key"],
                data_type=parameter["data_type"],
            )

    # TODO: Add Port type
    def create_ports(self, node, function):
        in_ports = NODE_FUNCTIONS_DEFINITIONS[function]["in_ports"]
        for ip in in_ports:
            InPort.objects.create(node=node, key=ip["key"])

        out_ports = NODE_FUNCTIONS_DEFINITIONS[function]["out_ports"]
        for op in out_ports:
            OutPort.objects.create(node=node, key=op["key"])


"""
class CredentialsParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialsParameter
        fields = ('id', 'credentials')
        read_only_fields = ('id', )
"""


class NodeUpdateSerializer(serializers.ModelSerializer):
    parameters = ParameterSerializer(many=True, required=False)
    in_ports = InPortSerializerInNode(many=True, required=False)
    # These out_ports can't actually be changed, but we include them so that they are returned in the response
    out_ports = InPortSerializerInNode(many=True, required=False)
    trigger_port = TriggerInPortSerializerInNode(many=False, allow_null=True)

    # Suggestions for the user
    # TODO: Use this
    # suggestions = serializers.SerializerMethodField()

    def get_suggestions(self, obj):
        refresh_flow_oauth2credentials(obj.flow)
        # Returns a list of suggestions by port
        in_ports_of_node = InPort.objects.filter(node__exact=obj).exclude(
            key__exact="trigger"
        )

        suggestions = {}
        for port in in_ports_of_node:
            suggestor = suggestions[port.key] = getattr(
                get_function(obj.function), f"suggest_{port.key}", None
            )
            if suggestor:
                suggestions[port.key] = suggestor(obj)

        return suggestions

    class Meta:
        model = Node
        fields = (
            "id",
            "flow",
            "name",
            "x",
            "y",
            "function",
            "parameters",
            "in_ports",
            "out_ports",
            "trigger_port",
            "credentials",
        )  # 'suggestions'
        read_only_fields = (
            "flow",
            "function",
        )  # 'suggestions'
        extra_kwargs = {"credentials": {"required": False}}
        """ 
        # This is needed when this serializer is called from within the FlowUpdate Serializer
        extra_kwargs = {
            'id': {'validators': []},
        }
        """

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.x = validated_data.get("x", instance.x)
        instance.y = validated_data.get("y", instance.y)

        credentials = validated_data.get("credentials")
        if credentials:
            if credentials.user == self.context["request"].user:
                instance.credentials = credentials

        if validated_data.get("parameters"):
            params_of_node = Parameter.objects.filter(node__exact=instance)
            for param in validated_data["parameters"]:
                param_instance = params_of_node.get(key__exact=param["key"])
                param_instance.value = param["value"]
                param_instance.save()

        if validated_data.get("in_ports"):
            in_ports_of_node = InPort.objects.filter(node__exact=instance)
            for port in validated_data["in_ports"]:
                port_instance = in_ports_of_node.get(key__exact=port["key"])
                # Check if a constant value already exists in db
                if hasattr(port_instance, "constant_value"):
                    # check if we want to update the constant value or delete it
                    if "constant_value" in port:
                        port_instance.constant_value.value = port["constant_value"][
                            "value"
                        ]
                        port_instance.constant_value.save()
                    else:
                        port_instance.constant_value.delete()
                else:
                    # check if we want to create a new constant value in db
                    if "constant_value" in port:
                        # we want to create a constant value, delete all edges that were connected to this port
                        connected_edges = Edge.objects.filter(
                            to_port__exact=port_instance
                        )
                        for edge in connected_edges:
                            edge.delete()
                        ConstantValue.objects.create(
                            value=port["constant_value"]["value"], port=port_instance
                        )

        # If the key exists, but the value is None we want to delete the port
        if "trigger_port" in validated_data.keys():
            if validated_data["trigger_port"] is None:
                TriggerInPort.objects.get(node__exact=instance).delete()
            else:
                create_trigger_port(instance)

        instance.save()
        # auto_create_trigger_port(instance)
        return instance


class EdgeSerializer(serializers.ModelSerializer):
    from_port = OutPortSerializer(many=False)
    to_port = BaseInPortMasterSerializer(many=False)

    class Meta:
        model = Edge
        fields = ("id", "from_port", "to_port")
        read_only_fields = ("id",)

    def create(self, validated_data):
        from_port_data = validated_data.pop("from_port")
        fp = OutPort.objects.filter(node__id__exact=from_port_data["node"].id).get(
            key__exact=from_port_data["key"]
        )

        to_port_data = validated_data.pop("to_port")
        if to_port_data["key"] == "trigger":
            tp = (
                TriggerInPort.objects.filter(node__id__exact=to_port_data["node"].id)
                .get(key__exact=to_port_data["key"])
                .baseinport
            )
        else:
            tp = (
                InPort.objects.filter(node__id__exact=to_port_data["node"].id)
                .get(key__exact=to_port_data["key"])
                .baseinport
            )

        from_node = Node.objects.get(id=from_port_data["node"].id)
        to_node = Node.objects.get(id=to_port_data["node"].id)
        if from_node == to_node:
            return
        if from_node.flow == to_node.flow:
            flow = Flow.objects.get(id=from_node.flow.id)
            cdata = {**validated_data, **{"to_port": tp, "from_port": fp, "flow": flow}}
            edge = Edge.objects.create(**cdata)
            return edge


class FlowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = ("id", "name", "owner")
        read_only_fields = ("id", "owner")


class FlowSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    nodes = NodeSerializer(many=True)
    edges = EdgeSerializer(many=True)
    # config = FlowConfigSerializer(many=False)

    class Meta:
        model = Flow
        fields = ("id", "nodes", "edges", "deployed")
        read_only_fields = ("id",)


class FlowUpdateSerializer(serializers.ModelSerializer):
    # This updater is only for fields like deployed, etc. NOT for nodes and edges
    class Meta:
        model = Flow
        fields = ("id", "nodes", "edges", "deployed")
        read_only_fields = ("id", "nodes", "edges")


class ShallowFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = ("id", "name")
        read_only_fields = ("id",)


class FlowRunCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowRun
        fields = (
            "id",
            "flow",
            "successful",
            "node_run_count",
            "datetime_start",
            "datetime_end",
            "message",
        )
        read_only_fields = (
            "id",
            "flow",
            "successful",
            "node_run_count",
            "datetime_start",
            "datetime_end",
            "message",
        )


class FlowRunSerializer(serializers.ModelSerializer):
    flow = ShallowFlowSerializer()

    class Meta:
        model = FlowRun
        fields = (
            "id",
            "flow",
            "successful",
            "node_run_count",
            "datetime_start",
            "datetime_end",
            "message",
        )
        read_only_fields = (
            "id",
            "flow",
            "successful",
            "node_run_count",
            "datetime_start",
            "datetime_end",
            "message",
        )


class NodeRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeRun
        fields = ("id", "node", "datetime_start", "datetime_end", "name", "function")
        read_only_fields = (
            "id",
            "node",
            "datetime_start",
            "datetime_end",
            "name",
            "function",
        )


class FlowRunWithNodeRunsSerializer(serializers.ModelSerializer):
    # More in depth serializer with unique node runs
    flow = ShallowFlowSerializer()
    node_runs = NodeRunSerializer(many=True)

    class Meta:
        model = FlowRun
        fields = (
            "id",
            "flow",
            "successful",
            "node_run_count",
            "datetime_start",
            "datetime_end",
            "message",
            "node_runs",
        )
        read_only_fields = (
            "id",
            "flow",
            "successful",
            "node_run_count",
            "datetime_start",
            "datetime_end",
            "message",
        )


class FlowRunUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowRun
        fields = (
            "id",
            "successful",
            "node_run_count",
            "datetime_start",
            "datetime_end",
        )
        read_only_fields = ("id",)


class NodeRunDataSerializer(serializers.Serializer):
    def to_representation(self, value):
        data = read_output_for_noderun(value)
        final = {}

        if data is None:
            final = {"error": {"type": "error", "data": str(value.flowrun.message)}}

        else:
            """
            # Convert np arrays to Pandas Series
            for output_key, output_data in data.items():
                if isinstance(output_data, np.ndarray):
                    data[output_key] = pd.Series(output_data)
            """

            for output_key, output_data in data.items():
                dtype = "serial"
                if isinstance(output_data, dict):
                    dtype = "serial"
                if isinstance(output_data, pd.DataFrame) or isinstance(
                    output_data, pd.Series
                ):
                    dtype = "tabular"
                    output_data = {
                        "values": output_data.fillna("[NULL]"),
                        "column_types": output_data.dtypes.apply(
                            lambda x: x.name
                        ).to_dict(),
                    }
                if dtype == "binary":
                    final[output_key] = {"type": dtype, "data": "Not serializable"}
                else:
                    final[output_key] = {"type": dtype, "data": output_data}
        return final


class TriggerSerializer(serializers.Serializer):
    class Meta:
        model = Trigger

        fields = ("id", "owner", "name", "enabled", "subscribed_nodes")
        read_only_fields = ("id", "owner")

    def to_representation(self, value):
        # Can't this be done nicer?
        if HttpEndpointTrigger.objects.filter(id__exact=value.id).exists():
            return HttpEndpointTriggerSerializer(
                instance=HttpEndpointTrigger.objects.get(id__exact=value.id)
            ).data
        elif TimerTrigger.objects.filter(id__exact=value.id).exists():
            return TimerTriggerSerializer(
                instance=TimerTrigger.objects.get(id__exact=value.id)
            ).data
        raise Exception("Unexpected type of trigger object")

    def to_internal_value(self, data):
        return super().to_internal_value(data)


class HttpEndpointTriggerSerializer(TriggerSerializer, serializers.ModelSerializer):
    class Meta:
        model = HttpEndpointTrigger
        fields = TriggerSerializer.Meta.fields + ("path",)
        read_only_fields = TriggerSerializer.Meta.read_only_fields

    def to_representation(self, value):
        return super().to_representation(value)


class TimerTriggerSerializer(TriggerSerializer, serializers.ModelSerializer):
    class Meta:
        model = TimerTrigger
        fields = TriggerSerializer.Meta.fields + ("interval", "repetitions")
        read_only_fields = TriggerSerializer.Meta.read_only_fields

    def to_representation(self, value):
        return super().to_representation(value)


class FlowConfigSerializer(serializers.ModelSerializer):
    # trigger = TriggerSerializer(many=False)

    class Meta:
        model = FlowConfig
        fields = ("log_node_run",)


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrontabSchedule
        fields = ("minute", "hour", "day_of_week", "day_of_month", "month_of_year")


class FlowRunScheduleSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer(many=False)

    class Meta:
        model = FlowRunSchedule
        fields = ("id", "schedule", "show_tz")
        read_only_fields = ("id",)
        # write_only_fields = ('flow',)

    def create(self, validated_data):
        schedule_data = validated_data.pop("schedule")
        crontab = ScheduleSerializer().create(schedule_data)
        flow = validated_data.pop("flow")
        flow_id_str = str(flow.id)
        now = str(datetime.datetime.now())
        periodic_task = PeriodicTask.objects.create(
            name=f"{flow_id_str} created {now}",
            crontab=crontab,
            task="core.tasks.dispatch_run_flow",
            args=json.dumps([flow_id_str]),
        )
        frs = FlowRunSchedule.objects.create(
            flow=flow,
            periodic_task=periodic_task,
            show_tz=validated_data.pop("show_tz"),
        )
        return frs
