import logging
import subprocess
import shlex

from coldfront.core.project.models import Project, ProjectAttribute
from coldfront.core.allocation.models import Allocation, AllocationAttribute, AllocationAttributeType

from coldfront.core.resource.models import Resource, ResourceType

from coldfront.core.utils.common import import_from_settings

logger = logging.getLogger(__name__)

STORAGE_NAME = import_from_settings("STORAGE_SYNC_STORAGE_RESOURCE_NAME")

# runs a given command
def _run_cmd(cmd):
    try:
        result = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        logger.warn(str(e))
    return result.stdout

# checks if an allocation is a storage allocation
def is_storage(allocation_pk):
    resource = Allocation.objects.get(pk=allocation_pk).get_parent_resource
    if resource.name == STORAGE_NAME:
        return True
    return False
    
# gets a storage allocation from a specified project
def get_allocation(project):
    ceph = Resource.objects.get(name=STORAGE_NAME, resource_type=ResourceType.objects.get(name="Storage"))
    alloc = None
    try:
        alloc = Allocation.objects.filter(project=project, resources=ceph)
        if alloc.count() > 1:
            alloc = alloc.order_by('id')
            alloc = alloc[0]
    except:
        logger.warn("Could not find allocation")
    return alloc

# sets the usage for a specified allocation and attriubute to a specified value
def set_usage(allocation, attribute_name, attribute_value):
    allocation.set_usage(attribute_name, attribute_value)
    allocation.save()

# gets all storage allocations
def get_storage_allocations():
    ceph = Resource.objects.get(name=STORAGE_NAME, resource_type=ResourceType.objects.get(name="Storage"))
    alloc = None
    try:
        alloc = Allocation.objects.filter(resources=ceph)
    except:
        logger.warn("Could not find allocation")
    return alloc

# gets the current usage for a storage allocation
def get_storage_usage(allocation):
    try:
        ps = subprocess.Popen(('df', "/shared/rc/" + allocation.project.title), stdout=subprocess.PIPE)
        bsize = subprocess.check_output(('awk', 'END { print $3 }'), stdin=ps.stdout)
        ps.wait
    except:
        return -1
    try:
        int(bsize)
    except:
        return -2
    gsize = int(bsize) // (10 ** 6)
    return int(gsize)
