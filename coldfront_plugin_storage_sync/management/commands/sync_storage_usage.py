import logging

from coldfront.core.project.models import Project, ProjectAttribute
from coldfront.core.allocation.models import Allocation, AllocationAttribute

from django.core.management.base import BaseCommand, CommandError

# from coldfront.core.allocation.models import (
#     Allocation,
#     AllocationAttribute,
#     AllocationAttributeType,
#     AllocationStatusChoice
# )

from coldfront_plugin_storage_sync.utils import (
    set_usage,
    get_storage_allocations,
    get_storage_usage
)

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "sync storage usage"
    
    def handle(self, *args, **options):
        allocations = get_storage_allocations()
        for alloc in allocations:
            #get and set usage
            usage = get_storage_usage(alloc)
            if usage >= 0:
                set_usage(alloc, "Storage Quota (GB)", usage)
            else:
                logger.warn("Storage share %s not found", allocation.project.title)
