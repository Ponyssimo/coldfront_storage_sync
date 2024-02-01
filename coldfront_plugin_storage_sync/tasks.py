from coldfront.core.allocation.models import Allocation

def add_storage_allocation(allocation_pk):
    allocation = Allocation.objects.get(pk=allocation_pk)
    project = allocation.project.name
    size = allocation.get_attribute("Storage Guota (GB)")

    # convert GB to bytes
    size = size * 1073741824

    #Figure out how to create CLAWS group and modify the autofs file here

    #run createDirectory and save exit code to status
    status = NULL

    #report error if status !=0
