from django.dispatch import receiver

from coldfront.core.allocation.signals import (allocation_activate)

@receiver(allocation_activate)
def activate_allocation(sender, **kwargs):
    pass
