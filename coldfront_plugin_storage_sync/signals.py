from django.dispatch import receiver
from django_q.tasks import async_task

from coldfront.core.allocation.signals import allocation_activate, allocation_change_approved, allocation_new

from coldfront.core.allocation.views import AllocationCreateView

def is_storage(allocation_pk):
    resource = Allocation.objects.get(allocation_pk).get_parent_resource
    if resource.name == 'CEPH':
        return True
    return False

#add default storage quota when allocation created, but before approved - allocation_new
@receiver(allocation_new)
def new_storage(sender, **kwargs):
    allocation_pk = kwargs.get('allocation_pk')
    if is_storage(allocation_pk):
        allocation = Allocation.objects.get(pk=allocation_pk)
        allocation.set_usage("Storage Quota (GB)", 150)

@receiver(allocation_activate)
@receiver(allocation_change_approved)
def activate_allocation(sender, **kwargs):
    allocation_pk = kwargs.get('allocation_pk')
    if is_storage(allocation_pk):
        async_task('coldfront_plugin_storage_sync.tasks.add_storage_allocation',allocation_pk)
