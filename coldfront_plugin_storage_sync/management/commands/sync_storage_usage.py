import logging

from coldfront.core.allocation.models import (
    Allocation,
    AllocationAttribute,
    AllocationAttributeType,
    AllocationStatusChoice
)

from coldfront_plugin_storage_sync.utils import (
    get_project,
    get_allocation,
    set_usage
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

        #need to get all allocations
        #loop through allocations, set usage based on the actual share
        #   implementation of getting the usage will need to comne later
