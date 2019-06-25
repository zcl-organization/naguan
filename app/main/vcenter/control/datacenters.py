# -*- coding=utf-8 -*-
from flask import g
from pyVim.task import WaitForTask
from pyVmomi import vim
from app.main.vcenter.control.utils import get_mor_name, get_connect, get_obj
from app.main.vcenter import db
from app.main.vcenter.utils.base import VCenter
from app.main.vcenter.control.datastores import sync_datastore


def sync_datacenter(vcenter_obj, dacenter_obj):
    dc_mor_name = get_mor_name(dacenter_obj)
    dc_host_moc = get_mor_name(dacenter_obj.hostFolder)
    dc_vm_moc = get_mor_name(dacenter_obj.vmFolder)

    # 同步dc
    # sync_datastore(vcenter_obj.platform, dacenter_obj, vcenter_obj.si, vcenter_obj.connect)
    # 获取dc的上一级信息
    dc_parent = db.vcenter.get_vcenter_tree_by_tree_type(vcenter_obj.platform['id'], 1)

    dc_exists = db.vcenter.check_if_dc_exists_by_dc_mor_name(vcenter_obj.platform['id'], dc_mor_name, 2)
    if dc_exists:
        dc_tree = db.vcenter.vcenter_tree_update(tree_type=2, platform_id=vcenter_obj.platform['id'],
                                                 name=dacenter_obj.name,
                                                 dc_mor_name=dc_mor_name, dc_oc_name=dacenter_obj.name,
                                                 mor_name=dc_mor_name,
                                                 dc_host_folder_mor_name=dc_host_moc, dc_vm_folder_mor_name=dc_vm_moc,
                                                 pid=dc_parent.id)
    else:
        dc_tree = db.vcenter.vcenter_tree_create(tree_type=2, platform_id=vcenter_obj.platform['id'],
                                                 name=dacenter_obj.name, dc_mor_name=dc_mor_name,
                                                 dc_oc_name=dacenter_obj.name,
                                                 mor_name=dc_mor_name, dc_host_folder_mor_name=dc_host_moc,
                                                 dc_vm_folder_mor_name=dc_vm_moc, pid=dc_parent.id)
    # TODO vcenter dc 资源数据同步
    data = dict(
        name=dacenter_obj.name, mor_name=dc_mor_name, platform_id=vcenter_obj.platform['id'],
        host_nums=0, vm_nums=0, cluster_nums=0, network_nums=0, datastore_nums=0,
        cpu_capacity=0, used_cpu=0, memory=0, used_memory=0, capacity=0, used_capacity=0,
    )
    # TODO 同步
    dc_local = db.datacenters.create_datacenter(**data)
    return dc_tree, dc_local


# def create_datacenter(platform_id, dc_name, folder=None):
#     si, content, platform = get_connect(platform_id)
#     # vcenter = VCenter(platform_id)
#     # if len(dc_name) > 80:
#     #     g.error_code = 4303
#     #     raise ValueError("The name of the datacenter must be under "
#     #                      "80 characters.")
#     dc = db.datacenters.get_dc_by_name(dc_name)  # 判断是否存在同名dc
#     if dc:
#         g.error_code = 4304
#         raise ValueError('The datacenter name already exists')
#     if folder is None:
#         folder = si.content.rootFolder
#     try:
#         if folder is not None and isinstance(folder, vim.Folder):
#             new_datacenter = folder.CreateDatacenter(name=dc_name)
#             try:
#                 vCenter_pid = get_vCenter_pid(platform)
#                 dc_mor_name = get_mor_name(new_datacenter)
#                 dc_host_moc = get_mor_name(new_datacenter.hostFolder)
#                 dc_vm_moc = get_mor_name(new_datacenter.vmFolder)
#                 # vcenter_tree同步
#                 vcenter_id = db.vcenter.vcenter_tree_create(tree_type=2, platform_id=platform_id,
#                                                             name=new_datacenter.name,
#                                                             dc_host_folder_mor_name=dc_host_moc,
#                                                             dc_mor_name=dc_mor_name, dc_oc_name=new_datacenter.name,
#                                                             dc_vm_folder_mor_name=dc_vm_moc, mor_name=dc_mor_name,
#                                                             cluster_mor_name=None, cluster_oc_name=None,
#                                                             pid=vCenter_pid)
#
#                 data = dict(
#                     name=new_datacenter.name, mor_name=dc_mor_name, platform_id=platform_id,
#                     host_nums=0, vm_nums=0, cluster_nums=0, network_nums=0, datastore_nums=0,
#                     cpu_capacity=0, used_cpu=0, memory=0, used_memory=0, capacity=0, used_capacity=0,
#                 )
#                 # datacenter同步
#                 dc_local = db.datacenters.create_datacenter(**data)
#                 return dc_local
#             except Exception as e:  # ???? 这个异常丢出的意义是什么
#                 g.error_code = 4305
#                 raise Exception('sync datacenters fail. %s' % str(e))
#     except Exception as e:
#         raise Exception('Failed to create datacenter. %s' % str(e))
#
#
# def del_datacenter(platform_id, dc_id):
#     si, content, platform = get_connect(platform_id)
#     dc = db.datacenters.get_dc_by_id(dc_id)
#     vcenter_tree_dc = db.vcenter.get_vcenter_obj_by_mor_name(platform_id, dc.mor_name)
#     # 判断本地datacenter下是否存在资源
#     clusters_obj = db.vcenter.get_clusters_from_dc(platform_id, vcenter_tree_dc.id)
#     if clusters_obj:
#         g.error_code = 4353
#         raise Exception('Resources exist under the local datacenter, unable to delete')
#     # 判断平台datacenter下是否存在资源
#     dc_obj = get_obj(content, [vim.Datacenter], dc.name)
#     clusters = dc_obj.hostFolder.childEntity
#     if clusters:
#         # 同步数据至本地
#         # sync_vcenter_tree(si, content, platform)
#         g.error_code = 4354
#         raise Exception('Resources exist under the vCenter datacenter, unable to delete')
#
#     dc_mor = get_mor_name(dc_obj)
#     # 任务销毁并等待
#     task = dc_obj.Destroy_Task()
#     WaitForTask(task)
#     # 删除本地数据库
#     db.vcenter.vcenter_tree_del_by_mor_name(platform_id, dc_mor)
#     db.datacenters.del_datacenter(dc_id)
#
#
# def find_datacenters(platform_id=None, dc_id=None, dc_name=None):
#     datacenters = db.datacenters.find_datacenters(platform_id, dc_id, dc_name)
#     dc_list = []
#     for dc in datacenters:
#         data = dict(
#             id=dc.id, name=dc.name, mor_name=dc.mor_name, platform_id=dc.platform_id,
#             host_nums=dc.host_nums, vm_nums=dc.vm_nums, cluster_nums=dc.cluster_nums,
#             network_nums=dc.network_nums, datastore_nums=dc.datastore_nums,
#             cpu_capacity=dc.cpu_capacity, used_cpu=dc.used_cpu, memory=dc.memory,
#             used_memory=dc.used_memory, capacity=dc.capacity, used_capacity=dc.used_capacity,
#         )
#         dc_list.append(data)
#     return dc_list
#
#     # return db.datacenters.get_datacenters(platform_id)
#
#
# # 获取Vcenter id
# def get_vCenter_pid(platform):
#     result = db.vcenter.vcenter_tree_get_by_platform(platform['id'], platform['platform_name'], 1)
#     if result:
#         vCenter_pid = result.id
#     else:
#         vCenter_pid = db.vcenter.vcenter_tree_create(tree_type=1, platform_id=platform['id'],
#                                                      name=platform['platform_name'])
#     return vCenter_pid


class DataCenter(object):
    def __init__(self, platform_id):
        self._platform_id = platform_id
        self._vCenter = VCenter(platform_id)

    def create(self, args):

        if db.datacenters.check_if_dc_exists_by_dc_name(args['dc_name']):
            g.error_code = 4304
            raise ValueError('The datacenter name already exists')

        folder = self._vCenter.si.content.rootFolder
        try:
            new_dc_obj = folder.CreateDatacenter(name=args['dc_name'])
        except Exception:
            raise RuntimeError('create new DataCenter failed')

        # TODO 同步dc信息到vcenter 表 以及 datacenter表
        dc_tree, dc_local = sync_datacenter(self._vCenter, new_dc_obj)
        return dc_local

    def delete(self, dc_id):
        import pdb
        pdb.set_trace()

        dc_info = db.datacenters.get_dc_by_id(dc_id)

        dc_tree = db.vcenter.get_vcenter_obj_by_mor_name(self._vCenter.platform['id'], dc_info.mor_name)

        # 判断本地datacenter下是否存在资源
        clusters_obj = db.vcenter.get_clusters_from_dc(self._vCenter.platform['id'], dc_tree.id)
        if clusters_obj:
            g.error_code = 4353
            raise Exception('Resources exist under the local datacenter, unable to delete')

        dc_obj = get_obj(self._vCenter.connect, [vim.Datacenter], dc_info.name)
        clusters = dc_obj.hostFolder.childEntity
        if clusters:
            # 同步数据至本地
            # sync_vcenter_tree(si, content, platform)
            g.error_code = 4354
            raise Exception('Resources exist under the vCenter datacenter, unable to delete')

        dc_mor = get_mor_name(dc_obj)
        # 任务销毁并等待
        task = dc_obj.Destroy_Task()
        WaitForTask(task)
        # 删除本地数据库
        db.vcenter.vcenter_tree_del_by_mor_name(self._vCenter.platform['id'], dc_mor)
        db.datacenters.del_datacenter(dc_id)

    def list(self, args):
        datacenters = db.datacenters.find_datacenters(self._vCenter.platform['id'], args['dc_id'], args['dc_name'])
        dc_list = []
        for dc in datacenters:
            data = dict(
                id=dc.id, name=dc.name, mor_name=dc.mor_name, platform_id=dc.platform_id,
                host_nums=dc.host_nums, vm_nums=dc.vm_nums, cluster_nums=dc.cluster_nums,
                network_nums=dc.network_nums, datastore_nums=dc.datastore_nums,
                cpu_capacity=dc.cpu_capacity, used_cpu=dc.used_cpu, memory=dc.memory,
                used_memory=dc.used_memory, capacity=dc.capacity, used_capacity=dc.used_capacity,
            )
            dc_list.append(data)
        return dc_list
