from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Flow, FlowConfig


@receiver(post_save, sender=Flow, dispatch_uid="create_flow_config")
def create_flow_config(sender, instance, created, **kwargs):
    if created:
        FlowConfig.objects.create(flow=instance)

