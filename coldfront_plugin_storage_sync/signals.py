from django.dispatch import receiver
from django_q.tasks import async_task

from coldfront.core.allocation.signals import allocation_activate, allocation_change_approved

from coldfront.core.allocation.views import AllocationCreateView

import logging

logger = logging.getLogger(__name__)

@receiver(allocation_activate)
@receiver(allocation_change_approved)
def activate_allocation(sender, **kwargs):
    logger.warn("test1")
    open("/tmp/test.txt", "x")
    #allocation_pk = kwargs.get('allocation_pk')
    #async_task('coldfront_plugin_storage_sync.tasks.add_storage_allocation',allocation_pk)
