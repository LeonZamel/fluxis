from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Flow, FlowConfig, FlowRun
from .tasks import dispatch_run_flow


@receiver(post_save, sender=Flow, dispatch_uid="create_flow_config")
def create_flow_config(sender, instance, created, **kwargs):
    if created:
        FlowConfig.objects.create(flow=instance)


"""
@receiver(post_save, sender=FlowRun, dispatch_uid="run_flow")
def run_flow(sender, instance, created, **kwargs):
    if created:
        # Dispatch via celery
        dispatch_run_flow.delay(instance.id)
"""
