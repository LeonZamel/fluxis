import json
import uuid
from datetime import datetime, time

from django.conf import settings
from django.db import models
from django_celery_beat.models import PeriodicTask
from authentication.models import Credentials

from .adapter import NODE_FUNCTIONS_CHOICES, PARAMETER_TYPE_CHOICES, PORT_TYPE_CHOICES

MAX_NAME_LENGTH = 100
MAX_DATASET_NAME_LENGTH = 200


class Flow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        "auth.User", related_name="flows", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    deployed = models.BooleanField(default=False)

    def __str__(self):
        return "Flow: {}, ID:{}".format(self.name, self.id)


class Node(models.Model):
    id = models.UUIDField(primary_key=True, blank=True, default=uuid.uuid4)
    flow = models.ForeignKey(Flow, related_name="nodes", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    x = models.IntegerField()
    y = models.IntegerField()
    function = models.CharField(max_length=40, choices=NODE_FUNCTIONS_CHOICES)
    credentials = models.ForeignKey(
        Credentials,
        related_name="node_credentials",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return "Node: {}, function: {}, ID:{}".format(self.name, self.function, self.id)


class Port(models.Model):
    # The node where a port belongs to is specified as a field in the InPort and OutPort class
    # The id should usually not be sent or used explicitly, as it is only for internal database purposes.
    # Instead, a port should be specified by its key and the node it belongs to, but Django currently does not support multiple fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=100)


class BaseInPort(Port):
    # Extra level of abstraction for trigger and regular in port
    # An edge is connected to this
    port = models.OneToOneField(Port, parent_link=True, on_delete=models.CASCADE)


class TriggerInPort(BaseInPort):
    # This is like an InPort but cannot have a constant value
    # We need this extra level of abstraction for the optional trigger port, which
    # is the only reason when this class is used, otherwise the InPort should be used
    base_in_port = models.OneToOneField(
        BaseInPort, parent_link=True, on_delete=models.CASCADE
    )

    # This is the optional trigger port that can be used. When all inputs
    # of a node have constant values, it is required and created
    # automatically
    # Is null on node if not used
    node = models.OneToOneField(
        Node, related_name="trigger_port", on_delete=models.CASCADE
    )


class InPort(BaseInPort):
    base_in_port = models.OneToOneField(
        BaseInPort, parent_link=True, on_delete=models.CASCADE
    )
    node = models.ForeignKey(Node, related_name="in_ports", on_delete=models.CASCADE)


class OutPort(Port):
    node = models.ForeignKey(Node, related_name="out_ports", on_delete=models.CASCADE)
    port = models.OneToOneField(Port, parent_link=True, on_delete=models.CASCADE)


class ConstantValue(models.Model):
    port = models.OneToOneField(
        InPort,
        primary_key=True,
        related_name="constant_value",
        on_delete=models.CASCADE,
    )
    data_type = models.CharField(
        choices=PORT_TYPE_CHOICES, max_length=20, default="string"
    )
    value = models.JSONField()


"""
class ConstantStringValue(ConstantValue):
    value = models.CharField(max_length=200)

class ConstantIntegerValue(ConstantValue):
    value = models.IntegerField()
"""


class Edge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow = models.ForeignKey(Flow, related_name="edges", on_delete=models.CASCADE)
    from_port = models.ForeignKey(OutPort, on_delete=models.CASCADE)
    # We must use the BaseInPort class here, so that a connection is possible
    # to the optional trigger port
    to_port = models.OneToOneField(BaseInPort, on_delete=models.CASCADE)


class Parameter(models.Model):
    node = models.ForeignKey(Node, related_name="parameters", on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    data_type = models.CharField(choices=PARAMETER_TYPE_CHOICES, max_length=20)
    value = models.JSONField()


"""
class CredentialsParameter(models.Model):
    node = models.OneToOneField(
        Node, related_name='credentials', on_delete=models.CASCADE)
    credentials = models.ForeignKey(OAuth2Credentials, related_name='node_parameter_credentials',
                                    on_delete=models.SET_NULL, null=True, blank=True, default=None)
"""


class FlowRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow = models.ForeignKey(
        Flow, related_name="runs", on_delete=models.SET_NULL, null=True
    )
    successful = models.BooleanField(blank=True, default=True)
    message = models.TextField(blank=True, null=True)
    node_run_count = models.IntegerField(blank=True, null=True)
    datetime_start = models.DateTimeField(blank=True, null=True)
    datetime_end = models.DateTimeField(blank=True, null=True)


class NodeRun(models.Model):
    node = models.ForeignKey(Node, null=True, on_delete=models.SET_NULL)
    flowrun = models.ForeignKey(
        FlowRun, related_name="node_runs", on_delete=models.CASCADE
    )
    datetime_start = models.DateTimeField(auto_now_add=True)
    datetime_end = models.DateTimeField(blank=True, null=True)
    output = models.FileField()
    # We store these as a copy of the node when it was run, so we can display it to the user
    name = models.CharField(max_length=100)
    function = models.CharField(max_length=40, choices=NODE_FUNCTIONS_CHOICES)


class NodeRunExtraOutput(models.Model):
    # We need this class when we have extra files as output, e.g. csv files
    noderun = models.ForeignKey(
        NodeRun, related_name="extra_output", on_delete=models.CASCADE
    )
    port_key = models.CharField(max_length=20)
    output = models.FileField()


class Trigger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        "auth.User", related_name="triggers", on_delete=models.CASCADE
    )
    subscribed_nodes = models.ManyToManyField(Node, blank=True)
    enabled = models.BooleanField(default=False)
    name = models.CharField(max_length=MAX_NAME_LENGTH)


class FlowRunSchedule(models.Model):
    flow = models.ForeignKey(Flow, related_name="schedule", on_delete=models.CASCADE)
    periodic_task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE)

    # This is only so we can display it to the user in the timezone they originally chose
    # Everything internally is UTC
    show_tz = models.CharField(max_length=50)

    @property
    def schedule(self):
        return self.periodic_task.crontab

    @schedule.setter
    def schedule(self, value):
        self.periodic_task.crontab = value
        self.periodic_task.save()

    @property
    def time(self):
        cron = self.periodic_task.crontab
        t = time(hour=int(cron.hour), minute=int(cron.minute))
        return t

    @time.setter
    def time(self, value):
        pass


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        "auth.User", related_name="files", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=MAX_DATASET_NAME_LENGTH)
    file = models.FileField()


class TimerTrigger(Trigger):
    # Interval in seconds
    interval = models.IntegerField()
    repetitions = models.IntegerField()


class HttpEndpointTrigger(Trigger):
    path = models.CharField(max_length=200)


class FlowConfig(models.Model):
    flow = models.OneToOneField(
        Flow, primary_key=True, related_name="config", on_delete=models.CASCADE
    )
    log_node_run = models.BooleanField(default=False)
    # trigger = models.ForeignKey(Trigger, related_name='trigger', on_delete=models.CASCADE, null=True, blank=True)
