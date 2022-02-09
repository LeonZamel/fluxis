# Celery tasks
from celery import shared_task

from .models import Flow, FlowRun
from .adapter import run_flow as adapter_run_flow

# TOD

class CeleryRunner:
    pass


@shared_task(ignore_result=True)
def dispatch_flowrun(flowrun_id):
    """
    Runs a flow
    """
    adapter_run_flow(flowrun_id)


@shared_task(ignore_result=True)
def dispatch_scheduled_flowrun(flow_id):
    """
    First creates the database object and then runs the flow.
    This way a run can be scheduled via celery beat
    """
    db_flow = Flow.objects.get(pk=flow_id)
    db_flowrun = FlowRun.objects.create(flow=db_flow)
    dispatch_flowrun.delay(db_flowrun.id)
