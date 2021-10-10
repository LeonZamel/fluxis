from dataclasses import asdict

from django.contrib.admin.utils import lookup_field
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session
from rest_framework import authentication, exceptions, generics, permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from core.adapter import NODE_FUNCTIONS_DEFINITIONS
from core.models import (
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
    OutPort,
    TimerTrigger,
    Trigger,
)
from core.tasks import dispatch_flowrun

from .serializers import (
    ConstantValueSerializer,
    EdgeSerializer,
    FlowConfigSerializer,
    FlowCreateSerializer,
    FlowRunCreateSerializer,
    FlowRunScheduleSerializer,
    FlowRunSerializer,
    FlowRunUpdateSerializer,
    FlowRunWithNodeRunsSerializer,
    FlowSerializer,
    FlowUpdateSerializer,
    HttpEndpointTriggerSerializer,
    InPortSerializer,
    NodeCreateSerializer,
    NodeRunDataSerializer,
    NodeRunSerializer,
    NodeSerializer,
    NodeUpdateSerializer,
    OutPortSerializer,
    ShallowFlowSerializer,
    TimerTriggerSerializer,
    TriggerSerializer,
    UserSerializer,
)


class LambdaCallbackAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        key = request.META.get("Authentication")
        if key != os.environ.get(SET_RUN_DATA_API_KEY, ""):
            raise exceptions.AuthenticationFailed("No such user")
        return (AnonymousUser(), None)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOfFlowInList(permissions.BasePermission):
    # TODO: Use this
    def has_permission(self, request, view):
        return Flow.objects.get(pk=view.kwargs["g_pk"]).owner == request.user


class IsOwnerOfFlow(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.flow.owner == request.user


class IsOwnerOfFlowRun(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.flowrun.flow.owner == request.user


class IsOwnerOfNode(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.node.flow.owner == request.user


class IsOwnerOfPort(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.port.node.flow.owner == request.user


"""
class RunFlowView(APIView):
    permission_classes = (IsOwner,)

    def get(self, request, format=None, **kwargs):
        flowid = kwargs['pk']
        db_flow = Flow.objects.get(pk=flowid)
        db_flowrun = FlowRun.objects.create(flow=db_flow)
        # config = FlowConfig.objects.get(flow__exact=flowid)
        run_flow_thread(flowid)
        return Response(status=status.HTTP_200_OK, data={'id': db_flowrun.id, 'datetime_start': db_flowrun.datetime_start})
"""

# We need to map the parameters, in_ports, out_ports, which are dataclasses, to dictionaries so they can be serialized
SERIALIZABLE_NODE_FUNCTIONS_DEFINITIONS = {}
for func_def in NODE_FUNCTIONS_DEFINITIONS.values():
    serialized_func_def = {}
    serialized_func_def["key"] = func_def.key
    serialized_func_def["category"] = func_def.category
    serialized_func_def["name"] = func_def.name
    serialized_func_def["parameters"] = list(map(asdict, func_def.parameters))
    serialized_func_def["in_ports"] = list(
        map(asdict, filter(lambda port: not port.internal, func_def.in_ports_conf))
    )
    serialized_func_def["out_ports"] = list(
        map(asdict, filter(lambda port: not port.internal, func_def.out_ports_conf))
    )
    serialized_func_def["credentials"] = (
        asdict(func_def.credentials) if func_def.credentials else None
    )
    SERIALIZABLE_NODE_FUNCTIONS_DEFINITIONS[func_def.key] = serialized_func_def


class InitView(APIView):
    def get(self, request, format=None):
        return Response(
            {
                "node_functions_definitions": SERIALIZABLE_NODE_FUNCTIONS_DEFINITIONS,
            }
        )


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class NodeList(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfFlow,
    )

    def get_queryset(self):
        if "g_pk" in self.kwargs:
            return Node.objects.filter(flow_id=self.kwargs["g_pk"])
        return Node.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NodeCreateSerializer
        return NodeSerializer

    def perform_create(self, serializer):
        serializer.save(flow=Flow.objects.get(pk=self.kwargs["g_pk"]))


class NodeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfFlow,
    )
    queryset = Node.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return NodeUpdateSerializer
        return NodeSerializer


class EdgeList(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfFlow,
    )
    serializer_class = EdgeSerializer

    def get_queryset(self):
        if "g_pk" in self.kwargs:
            return Edge.objects.filter(flow_id=self.kwargs["g_pk"])
        return Edge.objects.all()

    def perform_create(self, serializer):
        serializer.save(flow=Flow.objects.get(pk=self.kwargs["g_pk"]))


class EdgeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfFlow,
    )
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer


class FlowList(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )

    def get_queryset(self):
        return Flow.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return FlowCreateSerializer
        return ShallowFlowSerializer


class FlowDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flow.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return FlowUpdateSerializer
        return FlowSerializer


class FlowConfigDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfFlow,
    )
    queryset = FlowConfig.objects.all()
    serializer_class = FlowConfigSerializer


class ConstantValueList(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfPort,
    )
    queryset = ConstantValue.objects.all()
    serializer_class = ConstantValueSerializer


class ConstantValueDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfPort,
    )
    serializer_class = ConstantValueSerializer


# TODO: Finish http endpoint
class HttpEndpointDetail(APIView):
    def post(self, *args, **kwargs):
        req_object = None
        if "pk" in self.kwargs:
            req_object = HttpEndpointTrigger.objects.get(id=self.kwargs["pk"])
        else:
            return generics.Http404()
        for sn in req_object.subscribed_nodes.all():
            run_flow_thread(sn.flow.id, {sn.id: {"data_in": self.request.data.dict()}})
        return Response(status=status.HTTP_200_OK)


class HttpEndpointTriggerList(generics.ListCreateAPIView):
    permission_classes = (IsOwner,)
    queryset = HttpEndpointTrigger.objects.all()
    serializer_class = HttpEndpointTriggerSerializer

    # Use inheritance?
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TimerTriggerList(generics.ListCreateAPIView):
    permission_classes = (IsOwner,)
    queryset = TimerTrigger.objects.all()
    serializer_class = TimerTriggerSerializer

    # Use inheritance?
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TriggerList(generics.ListCreateAPIView):
    permission_classes = (IsOwner,)
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer

    # Use inheritance?
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FlowRunDetail(generics.RetrieveUpdateAPIView):
    # permission_classes = (IsOwnerOfFlow,)
    permission_classes = ()
    authentication_classes = ()
    queryset = FlowRun.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FlowRunWithNodeRunsSerializer
        elif self.request.method == "PATCH":
            return FlowRunUpdateSerializer
        return


"""
class FlowRunCreateList(generics.APIView):
    def post(self, *args, **kwargs):
        return FlowCreateView.as_view()

    def get(self, *args, **kwargs):
        return FlowCreateView.as_view()


class FlowCreateView(genertics.ListCreateAPIView):
"""


class FlowRunList(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfFlow,
    )
    serializer_class = FlowRunSerializer
    queryset = FlowRun.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            # This actually runs a flow
            return FlowRunCreateSerializer
        return FlowRunSerializer

    def get_queryset(self):
        owned_flows = Flow.objects.filter(owner=self.request.user)
        owned_flowruns = FlowRun.objects.filter(flow__in=owned_flows).order_by(
            "-datetime_start"
        )
        if "g_pk" in self.kwargs:
            return owned_flowruns.filter(flow_id__exact=self.kwargs["g_pk"])
        return owned_flowruns

    def perform_create(self, serializer):
        owned_flows = Flow.objects.filter(owner=self.request.user)
        flow = owned_flows.get(pk=self.kwargs["g_pk"])
        if flow:
            instance = serializer.save(flow=flow)
            # Dispatch via celery task
            dispatch_flowrun.delay(instance.id)
            # We don't have to return any instance or so, it will be accessed by the
            # create method via serializer.instance


class NodeRunDetail(generics.RetrieveAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfFlowRun,
    )
    serializer_class = NodeRunDataSerializer
    queryset = NodeRun.objects.all()


class FlowRunScheduleList(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfFlow,
    )
    serializer_class = FlowRunScheduleSerializer

    def get_queryset(self):
        frs = FlowRunSchedule.objects.filter(flow_id__exact=self.kwargs["g_pk"])
        return frs

    def perform_create(self, serializer):
        serializer.save(flow=Flow.objects.get(pk=self.kwargs["g_pk"]))


class FlowRunScheduleDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOfFlow,
    )
    serializer_class = FlowRunScheduleSerializer

    def get_queryset(self):
        frs = FlowRunSchedule.objects.filter(flow_id__exact=self.kwargs["g_pk"])
        return frs

    """
    def get_queryset(self):
        owned_flows = Flow.objects.filter(owner=self.request.user)
        if 'g_pk' in self.kwargs and 'r_pk' in self.kwargs and 'n_pk' in self.kwargs:
            return NodeRun.objects.filter(flowrun__exact=FlowRun.objects.filter(flow__in=owned_flows).get(id__exact=self.kwargs['r_pk'])).get(node_id__exact=self.kwargs['n_pk'])
        return 404
    """


class FileList(ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return FileCreateSerializer
        return FileSerializer


"""
class InPortDetailView(RetrieveAPIView):
    queryset = InPort.objects.all()
    serializer = InPortSerializer


class OutPortDetailView(RetrieveAPIView):
    queryset = OutPort.objects.all()
    serializer = OutPortSerializer
"""
