# -*- coding:utf-8 -*-
import time

from pyVmomi import vmodl
from pyVmomi import vim
from app.main.vcenter import db
from app.main.vcenter.control.utils import get_mor_name
from app.exts import celery

from app.main.vcenter.utils.base import VCenter
from app.main.vcenter.utils.vm_resource_pool import VMResourcePoolManager


@celery.task()
def sync_resourcepool(platform, dc, cluster, si, content):
    print ('sync_rp_start:', time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time())))
    obj = content.viewManager.CreateContainerView(dc, [vim.ResourcePool], True)
    resourcepools = obj.view

    for rp in resourcepools:

        rp_db = db.resource_pool.get_rp_by_mor_name(platform['id'], get_mor_name(rp))
        if isinstance(rp.parent, vim.ResourcePool):
            parent = db.resource_pool.get_resource_pool_by_datas(
                platform['id'], dc.name, cluster.name, rp.parent.name, get_mor_name(rp.parent))
            parent_id = parent.id
        else:
            parent_id = -1

        if rp_db:
            # print('update 1')
            update_resource_pool(rp_id=rp_db.id, platform_id=platform['id'], dc_name=dc.name,
                                 dc_mor_name=get_mor_name(dc), cluster_name=cluster.name,
                                 cluster_mor_name=get_mor_name(cluster), name=rp.name, mor_name=get_mor_name(rp),
                                 parent_name=rp.parent.name, parent_id=parent_id, over_all_status=rp.overallStatus,
                                 cpu_expand_able_reservation=rp.summary.config.cpuAllocation.expandableReservation,
                                 cpu_reservation=rp.summary.config.cpuAllocation.reservation,
                                 cpu_limit=rp.summary.config.cpuAllocation.limit,
                                 cpu_shares=rp.summary.config.cpuAllocation.shares.shares,
                                 cpu_level=rp.summary.config.cpuAllocation.shares.shares,
                                 cpu_over_all_usage=rp.summary.runtime.cpu.overallUsage,
                                 cpu_max_usage=rp.summary.runtime.cpu.maxUsage,
                                 memory_expand_able_reservation=rp.summary.config.memoryAllocation.expandableReservation,
                                 memory_reservation=rp.summary.config.memoryAllocation.reservation,
                                 memory_limit=rp.summary.config.memoryAllocation.limit,
                                 memory_shares=rp.summary.config.memoryAllocation.shares.shares,
                                 memory_level=rp.summary.config.memoryAllocation.shares.level,
                                 memory_over_all_usage=rp.summary.runtime.memory.overallUsage,
                                 memory_max_usage=rp.summary.runtime.memory.maxUsage)
            # print('update 2')
        else:
            # print('create 1')
            create_resource_pool(platform_id=platform['id'], dc_name=dc.name,
                                 dc_mor_name=get_mor_name(dc), cluster_name=cluster.name,
                                 cluster_mor_name=get_mor_name(cluster), name=rp.name, mor_name=get_mor_name(rp),
                                 parent_name=rp.parent.name, parent_id=parent_id, over_all_status=rp.overallStatus,
                                 cpu_expand_able_reservation=rp.summary.config.cpuAllocation.expandableReservation,
                                 cpu_reservation=rp.summary.config.cpuAllocation.reservation,
                                 cpu_limit=rp.summary.config.cpuAllocation.limit,
                                 cpu_shares=rp.summary.config.cpuAllocation.shares.shares,
                                 cpu_level=rp.summary.config.cpuAllocation.shares.shares,
                                 cpu_over_all_usage=rp.summary.runtime.cpu.overallUsage,
                                 cpu_max_usage=rp.summary.runtime.cpu.maxUsage,
                                 memory_expand_able_reservation=rp.summary.config.memoryAllocation.expandableReservation,
                                 memory_reservation=rp.summary.config.memoryAllocation.reservation,
                                 memory_limit=rp.summary.config.memoryAllocation.limit,
                                 memory_shares=rp.summary.config.memoryAllocation.shares.shares,
                                 memory_level=rp.summary.config.memoryAllocation.shares.level,
                                 memory_over_all_usage=rp.summary.runtime.memory.overallUsage,
                                 memory_max_usage=rp.summary.runtime.memory.maxUsage)

        db.instances.clean_all_vm_rp_name_by_rp_name(platform['id'], rp.name)
    print ('sync_rp_end:', time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time())))


def create_resource_pool(platform_id, dc_name, dc_mor_name, cluster_name,
                         cluster_mor_name, name, mor_name, parent_name, parent_id, over_all_status,
                         cpu_expand_able_reservation,
                         cpu_reservation, cpu_limit, cpu_shares, cpu_level, cpu_over_all_usage, cpu_max_usage,
                         memory_expand_able_reservation, memory_reservation, memory_limit, memory_shares, memory_level,
                         memory_over_all_usage, memory_max_usage):
    db.resource_pool.create_resource_pool(platform_id, dc_name, dc_mor_name, cluster_name, cluster_mor_name, name,
                                          mor_name, parent_name, parent_id, over_all_status, cpu_expand_able_reservation,
                                          cpu_reservation, cpu_limit, cpu_shares,
                                          cpu_level, cpu_over_all_usage, cpu_max_usage, memory_expand_able_reservation,
                                          memory_reservation, memory_limit, memory_shares, memory_level,
                                          memory_over_all_usage, memory_max_usage)


def update_resource_pool(rp_id, platform_id, dc_name, cluster_name, cluster_mor_name, dc_mor_name, name, mor_name,
                         parent_name, parent_id,
                         over_all_status, cpu_expand_able_reservation,
                         cpu_reservation, cpu_limit, cpu_shares, cpu_level, cpu_over_all_usage, cpu_max_usage,
                         memory_expand_able_reservation, memory_reservation, memory_limit, memory_shares,
                         memory_level, memory_over_all_usage, memory_max_usage):
    db.resource_pool.update_resource_pool(rp_id, platform_id, dc_name, dc_mor_name, cluster_name, cluster_mor_name,
                                          name, mor_name, parent_name, parent_id, over_all_status, cpu_expand_able_reservation,
                                          cpu_reservation, cpu_limit, cpu_shares, cpu_level, cpu_over_all_usage,
                                          cpu_max_usage, memory_expand_able_reservation,
                                          memory_reservation, memory_limit, memory_shares, memory_level,
                                          memory_over_all_usage, memory_max_usage)


def get_resource_pool_list(platform_id, dc_mor_name, cluster_mor_name):
    results = db.resource_pool.get_resource_pool_list(platform_id, dc_mor_name, cluster_mor_name)

    resource_list = []
    for result in results:
        _t = {
            'id': result.id,
            'platform_id': result.platform_id,
            'dc_name': result.dc_name,
            'dc_mor_name': result.dc_mor_name,
            'cluster_name': result.cluster_name,
            'cluster_mor_name': result.cluster_mor_name,
            'name': result.name,
            'mor_name': result.mor_name,
            'parent_name': result.parent_name,
            'over_all_status': result.over_all_status,
            'cpu_expand_able_reservation': result.cpu_expand_able_reservation,
            'cpu_reservation': result.cpu_reservation,
            'cpu_limit': result.cpu_limit,
            'cpu_shares': result.cpu_shares,
            'cpu_level': result.cpu_level,
            'cpu_over_all_usage': result.cpu_over_all_usage,
            'cpu_max_usage': result.cpu_max_usage,
            'memory_expand_able_reservation': result.memory_expand_able_reservation,
            'memory_reservation': result.memory_reservation,
            'memory_limit': result.memory_limit,
            'memory_shares': result.memory_shares,
            'memory_level': result.memory_level,
            'memory_over_all_usage': result.memory_over_all_usage,
            'memory_max_usage': result.memory_max_usage
        }
        resource_list.append(_t)
    return resource_list


def check_if_resource_pool_exists(resouce_pool_id=None, dc_name=None, cluster_name=None, resource_pool_name=None, root_rp_name=None):
    if resouce_pool_id:
        return True if db.resource_pool.get_resource_pool_by_id(resouce_pool_id) else False
    elif dc_name and cluster_name and resource_pool_name:
        root_rp_name = root_rp_name if root_rp_name else 'Resources'   # 如果没有给定root_rp_name对象即认为是在集群根目录下创建
        return True if db.resource_pool.get_resource_pool_by_names(dc_name, cluster_name, resource_pool_name, root_rp_name) else False
    else:
        raise RuntimeError


class ResourcePool:
    def __init__(self, platform_id):
        self._platform_id =  platform_id
        self._vcenter = VCenter(platform_id)

    def create_pool(self, cluster_name, data_center_name, rp_name, root_rp_id, **kw_args):
        """
        创建
        """
        # 默认在根目录下创建 root_rp=None
        root_rp = None if root_rp_id == -1 or not root_rp_id else db.resource_pool.get_resource_pool_by_id(root_rp_id)
        # 获取根节点名称
        root_rp_name = root_rp.name if root_rp else None
        cluster = self._vcenter.find_cluster_by_name(cluster_name)
        root_rp_obj = self._find_resource_pool_by_name(cluster, root_rp.mor_name) if root_rp else None

        if check_if_resource_pool_exists(
                dc_name=data_center_name, cluster_name=cluster_name, 
                resource_pool_name=rp_name, root_rp_name=root_rp_name):
            raise RuntimeError('This ResourcePool Exists')

        _vmrpm = VMResourcePoolManager(cluster)
        if not _vmrpm.create(rp_name, root_resource_pool=root_rp_obj, **kw_args):
            raise RuntimeError('Create ResourcePool Failed!!!')

        # 同步操作  获取dc、rp对象 保存数据
        dc = self._find_data_center_by_cluster(cluster)
        rp = self._find_rp_by_parent(root_rp_obj, cluster, rp_name)  # 一定会找到 emmm
        parent = db.resource_pool.get_resource_pool_by_datas(
            self._vcenter.platform['id'], dc.name, cluster.name, rp.parent.name, get_mor_name(rp.parent))
        parent_id = parent.id
        args_dict = dict(
            platform_id=self._vcenter.platform['id'],
            dc_name=dc.name,
            dc_mor_name=get_mor_name(dc),
            cluster_name=cluster.name,
            cluster_mor_name=get_mor_name(cluster),
            name=rp.name,
            mor_name=get_mor_name(rp),
            parent_name=rp.parent.name,
            parent_id=parent_id,
            over_all_status=rp.overallStatus,
            cpu_expand_able_reservation=rp.summary.config.cpuAllocation.expandableReservation,
            cpu_reservation=rp.summary.config.cpuAllocation.reservation,
            cpu_limit=rp.summary.config.cpuAllocation.limit,
            cpu_shares=rp.summary.config.cpuAllocation.shares.shares,
            cpu_level=rp.summary.config.cpuAllocation.shares.shares,
            cpu_over_all_usage=rp.summary.runtime.cpu.overallUsage,
            cpu_max_usage=rp.summary.runtime.cpu.maxUsage,
            memory_expand_able_reservation=rp.summary.config.memoryAllocation.expandableReservation,
            memory_reservation=rp.summary.config.memoryAllocation.reservation,
            memory_limit=rp.summary.config.memoryAllocation.limit,
            memory_shares=rp.summary.config.memoryAllocation.shares.shares,
            memory_level=rp.summary.config.memoryAllocation.shares.level,
            memory_over_all_usage=rp.summary.runtime.memory.overallUsage,
            memory_max_usage=rp.summary.runtime.memory.maxUsage
        )
        create_resource_pool(**args_dict)

    def delete_pool(self, cluster_name, del_rp_mor_name):
        """
        删除动作  不包括同步
        """
        cluster = self._vcenter.find_cluster_by_name(cluster_name)
        _vmrpm = VMResourcePoolManager(cluster)
        if not _vmrpm.destroy(del_rp_mor_name):
            raise RuntimeError('Destory ResourcePool Failed!!!')

    def delete_pool_by_id(self, rp_id):
        """
        删除动作 包括同步
        """
        if not check_if_resource_pool_exists(resouce_pool_id=rp_id):
            raise RuntimeError('This ResourcePool Not Exists')

        pool = db.resource_pool.get_resource_pool_by_id(rp_id)
        self.delete_pool(pool.cluster_name, pool.mor_name)

        # 同步
        db.resource_pool.delete_resource_pool(rp_id)

    def _find_data_center_by_cluster(self, cluster):
        """
        通过cluster查找数据中心   cluster.parent -> vim.Folder
        """
        cluster_networks = set(cluster.network)
        container = self._vcenter.connect.viewManager.CreateContainerView(
            self._vcenter.connect.rootFolder, [vim.Datacenter], True)
        for item in container.view:
            if not (cluster_networks - set(item.network)):
                return item

        return None

    def _find_resource_pool_by_name(self, cluster, rp_mor_name):
        """
        通过名称查询资源池对象
        """
        resource_pools = [cluster.resourcePool,]
        for item in resource_pools:
            if isinstance(item, vim.ResourcePool):
                if get_mor_name(item) == rp_mor_name:
                    return item
                if item.resourcePool:
                    if isinstance(item.resourcePool, list):
                        resource_pools.extend(item.resourcePool)
                    else:
                        resource_pools.append(item.resourcePool)
        return None

    def _find_rp_by_parent(self, root_rp, cluster, rp_name):
        """
        通过父节点查找资源池对象
        """
        if not root_rp:
            root_rp = cluster.resourcePool
        
        for item in root_rp.resourcePool:
            if item.name == rp_name:
                return item
        
        return None
