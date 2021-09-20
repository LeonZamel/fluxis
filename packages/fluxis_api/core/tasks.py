# Celery tasks
from celery import shared_task

from .models import Flow, FlowRun
from .adapter import run_flow as adapter_run_flow


@shared_task(ignore_result=True)
def dispatch_run_flow(db_flow_id):
    """
    First creates the database object and then runs the flow.
    This way a run can be scheduled via celery beat
    """
    db_flow = Flow.objects.get(pk=db_flow_id)
    db_flowrun = FlowRun.objects.create(flow=db_flow)
    adapter_run_flow(db_flowrun.id)
