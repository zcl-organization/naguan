# -*- coding: utf-8 -*-
from pyVmomi import pyVmomi
from pyVim.task import WaitForTask


class VMResourcePoolManager:
    def __init__(self, data_center, cluster):
        self._data_center = data_center
        self._cluster = cluster

    def create(self, rp_name):
        rp_spec = vim.ResourceConfigSpec()

        cpu_alloc = vim.ResourceAllocationInfo()
        cpu_alloc.expandableReservation = self.cpu_expandable_reservations
        cpu_alloc.limit = int(self.cpu_limit)
        cpu_alloc.reservation = int(self.cpu_reservation)
        cpu_alloc_shares = vim.SharesInfo()
        cpu_alloc_shares.level = self.cpu_shares
        cpu_alloc.shares = cpu_alloc_shares
        rp_spec.cpuAllocation = cpu_alloc

        mem_alloc = vim.ResourceAllocationInfo()
        mem_alloc.limit = int(self.mem_limit)
        mem_alloc.expandableReservation = self.mem_expandable_reservations
        mem_alloc.reservation = int(self.mem_reservation)
        mem_alloc_shares = vim.SharesInfo()
        mem_alloc_shares.level = self.mem_shares
        mem_alloc.shares = mem_alloc_shares
        rp_spec.memoryAllocation = mem_alloc

        # self.dc_obj = find_datacenter_by_name(self.content, self.datacenter)
        # self.cluster_obj = find_cluster_by_name(self.content, self.cluster, datacenter=self.dc_obj)
                
        # rootResourcePool = self._cluster.resourcePool
        self._cluster.resourcePool.CreateResourcePool(rp_name, rp_spec)

    def destroy(self, rp_name):
        resource_pool = self._find_resource_pool_by_name(rp_name)
        
        task = self.resource_pool_obj.Destroy()
        success, result = wait_for_task(task)

    def _find_resource_pool_by_name(self, name):
        rp_obj = ''
        return rp_obj
