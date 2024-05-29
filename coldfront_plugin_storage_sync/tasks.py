import logging
from coldfront.core.allocation.models import Allocation, AllocationAttribute
from coldfront.core.project.models import Project, ProjectAttribute
from coldfront.core.utils.common import import_from_settings

from coldfront_plugin_storage_sync.utils import run_cmd

logger = logging.getLogger(__name__)

def add_storage_allocation(allocation_pk):
    allocation = Allocation.objects.get(pk=allocation_pk)
    share = allocation.project.title
    data_found = True
    if not share:
        logger.warn("No project name found")
        data_found = False
    size = allocation.get_attribute("Storage Quota (GB)")
    if not size:
        logger.warn("No allocation size found")
        data_found = False

    if not data_found:
        logger.warn("Storage share could not be added/modified")
        exit()

    # convert GB to bytes
    byteSize = size * 1073741824

    # run createDirectory and save exit code to status, may also change to running in python depending on how things get done
    result, resulterr, resultcode = run_cmd("/usr/local/sbin/createDirectory.sh")
    
    logger.info(result + ', ' + resultcode) # in for testing

    #report error if status !=0
    if status == 1:
        logger.warn("Failed adding or changing allocation: no project name found")
    elif status == 2:
        logger.warn("Failed adding or changing allocation: no allocation size found")
    elif status == 3:
        logger.info("%s already has storage quota of %dGB", share, size)
    else:
        logger.info("Successfully added or changed allocation %s with size %d", share, size)
