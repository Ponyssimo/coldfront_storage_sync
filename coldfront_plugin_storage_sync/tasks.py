import logging
from coldfront.core.allocation.models import Allocation

logger = logging.getLogger(__name__)

def add_storage_allocation(allocation_pk):
    logger.info("test")
    allocation = Allocation.objects.get(pk=allocation_pk)
    logger.info("allocation")
    try:
        share = allocation.get_attribute("Storage_Group_Name")
    except:
        logger.warn("Failed adding or changing allocation: no project name found")
        exit
    logger.info("name: %s", share)
    try:
        size = allocation.get_attribute("Storage Quota (GB)")
    except:
        logger.warn("Failed adding or changing allocation: no allocation size found")
        exit
    logger.info("size: %i", size)

    # convert GB to bytes
    byteSize = size * 1073741824

    #Figure out how to create CLAWS group and modify the autofs file here

    #run createDirectory and save exit code to status
    status = 0

    share = "test"
    size = 3

    #report error if status !=0
    if status == 1:
        logger.warn("Failed adding or changing allocation: no project name found")
    elif status == 2:
        logger.warn("Failed adding or changing allocation: no allocation size found")
    elif status == 3:
        logger.info("%s already has storage quota of %dGB", share, size)
    else:
        logger.info("Successfully added or changed allocation %s with size %d", share, size)
