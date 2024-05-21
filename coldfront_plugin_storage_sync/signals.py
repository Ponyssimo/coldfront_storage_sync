import logging
from django.dispatch import receiver
from django_q.tasks import async_task

from coldfront.core.allocation.signals import allocation_activate, allocation_change_approved, allocation_new
from coldfront.core.resource.models import Resource, ResourceAttribute, ResourceAttributeType
from coldfront.core.allocation.models import Allocation,AllocationAttribute,AllocationAttributeType,AllocationStatusChoice
from coldfront.core.project.models import Project, ProjectAttribute

from coldfront.core.allocation.views import AllocationCreateView

from coldfront.core.utils.common import import_from_settings

from coldfront_plugin_storage_sync.utils import is_storage

logger = logging.getLogger(__name__)

DEFAULT_QUOTA = import_from_settings("STORAGE_SYNC_DEFAULT_QUOTA")

# add default storage quota and set usage to 0 when allocation created, but before approved
@receiver(allocation_new)
def new_storage(sender, **kwargs):
    allocation_id = kwargs.get('allocation_pk')
    allocation_obj = Allocation.objects.get(id=allocation_id)
    if is_storage(allocation_id):
        allocation = Allocation.objects.get(pk=allocation_id)
        sq = AllocationAttributeType.objects.get(name="Storage Quota (GB)")
        storage_quota = AllocationAttribute.objects.filter(allocation=allocation_id, allocation_attribute_type=sq)
        storage_quota = AllocationAttribute(allocation=allocation_obj, allocation_attribute_type=sq, value=DEFAULT_QUOTA)
        allocation.set_usage("Storage Quota (GB)", 0)
        storage_quota.save()
        logger.info("changed storage allocation quota for %s to %d", allocation_obj.project.title, DEFAULT_QUOTA)

# create project directory or modify quota when allocation created or a change is approved
@receiver(allocation_activate)
@receiver(allocation_change_approved)
def activate_allocation(sender, **kwargs):
    allocation_pk = kwargs.get('allocation_pk')
    if is_storage(allocation_pk):
        async_task('coldfront_plugin_storage_sync.tasks.add_storage_allocation',allocation_pk)
