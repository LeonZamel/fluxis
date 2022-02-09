from django.contrib import admin

from .models import Node, Edge, Flow, TriggerInPort, InPort, OutPort, HttpEndpointTrigger, TimerTrigger, ConstantValue, FlowConfig, FlowRun, NodeRun

# Register your models here.
admin.site.register(Node)
admin.site.register(Edge)
admin.site.register(Flow)
admin.site.register(InPort)
admin.site.register(TriggerInPort)
admin.site.register(OutPort)
admin.site.register(HttpEndpointTrigger)
admin.site.register(TimerTrigger)
admin.site.register(ConstantValue)
admin.site.register(FlowConfig)
admin.site.register(FlowRun)
admin.site.register(NodeRun)
