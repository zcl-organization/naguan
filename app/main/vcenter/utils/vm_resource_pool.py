# -*- coding: utf-8 -*-
from pyVmomi import vim
from pyVmomi import pyVmomi
from pyVim.task import WaitForTask

from app.main.vcenter.control.utils import get_mor_name


class VMResourcePoolManager:
    def __init__(self, cluster):
        self._cluster = cluster

    def create(self, rp_name, root_resource_pool=None, **kw_args):
        rp_spec = vim.ResourceConfigSpec()

        cpu_alloc = vim.ResourceAllocationInfo()
        cpu_alloc.expandableReservation = kw_args.get('cpu_expandableReservation', True)
        cpu_alloc.limit = int(kw_args.get('cpu_limit', -1))
        cpu_alloc.reservation = int(kw_args.get('cpu_reservation', 0))
        cpu_alloc_shares = vim.SharesInfo()
        cpu_alloc_shares.level = kw_args.get('cpu_share', 'normal')
        cpu_alloc.shares = cpu_alloc_shares
        rp_spec.cpuAllocation = cpu_alloc

        mem_alloc = vim.ResourceAllocationInfo()
        mem_alloc.limit = int(kw_args.get('mem_limit', -1))
        mem_alloc.expandableReservation = kw_args.get('mem_expandableReservation', True)
        mem_alloc.reservation = int(kw_args.get('mem_reservation', 0))
        mem_alloc_shares = vim.SharesInfo()
        mem_alloc_shares.level = kw_args.get('mem_share', 'normal')
        mem_alloc.shares = mem_alloc_shares
        rp_spec.memoryAllocation = mem_alloc

        if root_resource_pool is None:
            root_resource_pool = self._cluster.resourcePool

        try:
            root_resource_pool.CreateResourcePool(rp_name, rp_spec)
        except Exception as e:
            return False
        
        return True

    def destroy(self, rp_name):
        try:
            resource_pool = self._find_resource_pool_by_name(rp_name)

            if not resource_pool:
                raise RuntimeError('Not the Resource Pool, Name: {}'.format(rp_name))
            WaitForTask(resource_pool.Destroy())
        except Exception as e:
            print e
            return False 

        return True

    def _find_resource_pool_by_name(self, mor_name):
        resource_pools = [item for item in self._cluster.resourcePool.resourcePool]
        for item in resource_pools:
            if isinstance(item, vim.ResourcePool):
                if get_mor_name(item) == mor_name:
                    return item
                if item.resourcePool:
                    resource_pools.extend(item.resourcePool)
        return None
