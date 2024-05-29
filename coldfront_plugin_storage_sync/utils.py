import logging
import subprocess

from coldfront.core.project.models import Project
from coldfront.core.allocation.models import Allocation, AllocationAttribute, AllocationAttributeType

from coldfront.core.resource.models import Resource, ResourceType

logger = logging.getLogger(__name__)
STORAGE_NAME = "CEPH"

def run_cmd(cmd):
    try:
        result = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        logger.warn(str(e))
    return result.stdout, result.stderr, result.returncode

def is_storage(allocation_pk):
    resource = Allocation.objects.get(pk=allocation_pk).get_parent_resource
    if resource.name == STORAGE_NAME:
        return True
    return False
    
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
    
def set_usage(allocation, attribute_name, attribute_value):
    allocation.set_usage(attribute_name, attribute_value)
    allocation.save()

def get_storage_allocations():
    ceph = Resource.objects.get(name=STORAGE_NAME, resource_type=ResourceType.objects.get(name="Storage"))
    alloc = None
    try:
        alloc = Allocation.objects.filter(resources=ceph)
    except:
        logger.warn("Could not find allocation")
    return alloc

def get_storage_usage(allocation):
    return 50
