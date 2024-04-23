import logging

from coldfront.core.allocation.models import (
    Allocation,
    AllocationAttribute,
    AllocationAttributeType,
    AllocationStatusChoice)

from coldfront_plugin_storage_sync.utils import (
    get_project,
    get_allocation,
    set_usage
)

logger = logging.getLogger(__name__)


