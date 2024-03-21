import logging
from coldfront.core.allocation.models import Allocation
import subprocess

logger = logging.getLogger(__name__)

def add_storage_allocation(allocation_pk):
    allocation = Allocation.objects.get(pk=allocation_pk)
    share = allocation.get_attribute("Storage_Group_Name")
    if not share:
        logger.warn("Failed adding or changing allocation: no project name found")
        exit
    size = allocation.get_attribute("Storage Quota (GB)")
    if not size:
        logger.warn("Failed adding or changing allocation: no allocation size found")
        exit

    # convert GB to bytes
    byteSize = size * 1073741824

    #Figure out how to create CLAWS group and modify the autofs file here

    #run createDirectory and save exit code to status
    result = subprocess.run(['ssh', 'gung.rc.rit.edu', "whoami"], 
                            shell=False, 
                            stdin=stdin, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            check=check)
    logger.info("test")
    logger.info(result)
    status = 0

    #report error if status !=0
    if status == 1:
        logger.warn("Failed adding or changing allocation: no project name found")
    elif status == 2:
        logger.warn("Failed adding or changing allocation: no allocation size found")
    elif status == 3:
        logger.info("%s already has storage quota of %dGB", share, size)
    else:
        logger.info("Successfully added or changed allocation %s with size %d", share, size)
