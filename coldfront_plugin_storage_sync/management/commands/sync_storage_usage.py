import logging

from django.core.management.base import BaseCommand, CommandError

from coldfront.core.allocation.models import (
    Allocation,
    AllocationAttribute,
    AllocationAttributeType,
    AllocationStatusChoice
)

from coldfront_plugin_storage_sync.utils import (
    get_storage_allocations,
    get_allocation,
    set_usage,
    get_storage_allocations,
    get_storage_usage
)

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "sync storage usage"
    def add_arguments(self, parser):
        parser.add_argument("-n", "--noop", help="Print commands only. Do not run any commands.", action="store_true")
    
    def handle(self, *args, **options):
        self.noop = False
        if options['noop']:
            self.noop = True
            logger.warn("No operations will be committed")
        allocations = get_storage_allocations()
        for alloc in allocations:
            #get and set usage
            usage = get_storage_usage(alloc)
            set_usage(alloc, "Storage Quota (GB)", usage)
