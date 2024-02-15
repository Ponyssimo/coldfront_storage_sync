import logging
from coldfront.core.allocation.models import Allocation

def add_storage_allocation(allocation_pk):
    allocation = Allocation.objects.get(pk=allocation_pk)
    project = allocation.get_attribute("Storage_Group_Name")
    size = allocation.get_attribute("Storage Guota (GB)")

    # convert GB to bytes
    size = size * 1073741824

    #Figure out how to create CLAWS group and modify the autofs file here

    #run createDirectory and save exit code to status
    status = NULL

    #report error if status !=0
    if status == 1:
        logger.error("Failed adding or changing allocation: no project name found")
    elif status == 2:
        logger.error("Failed adding or changing allocation: no allocation size found")

    logger.info("Successfully added or changed allocation %s with size %d", project, size)
