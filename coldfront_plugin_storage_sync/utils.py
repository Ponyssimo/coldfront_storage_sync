import logging
import subprocess

from coldfront.core.project.models import Project
from coldfront.core.allocation.models import Allocation, AllocationAttribute, AllocationAttributeType

from coldfront.core.resource.models import Resource, ResourceType

logger = logging.getLogger(__name__)

def _run_cmd(cmd):
    try:
        result = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        logger.warn(str(e))
    return result.stdout
    
def get_project(project_name):
    proj = None
    try:
        proj = Project.objects.filter(title=project_name).get()
    except:
        logger.warn("Could not find project")
    return proj
    
def get_allocation(project):
    ceph = Resource.objects.get(name="CEPH", resource_type=ResourceType.objects.get(name="Storage"))
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
    pass

def get_storage_usage(allocation):
    pass
