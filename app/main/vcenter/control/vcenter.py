# -*- coding:utf-8 -*-
import datetime

from app.main.vcenter.control.resource_pool import sync_resourcepool
from app.main.vcenter.control.utils import get_mor_name, connect_server, get_connect
from app.main.vcenter.control.network_port_group import sync_network_port_group
from app.main.vcenter.control import network_devices as netowrk_device_manage
from app.main.vcenter.control import disks as disk_manage
from app.main.vcenter import db
from app.main.vcenter.control.datastores import sync_datastore
from app.main.vcenter.control.snapshots import sync_snapshot
from pyVim import connect
import atexit
from flask import g
import time
# import threadpool
# import threading

from pyVmomi import vmodl
from pyVmomi import vim

from app.exts import celery
from app.main.base import task
from app.main.base.control import task_logs


@celery.task(base=task.tasks_log.SyncTreeCall)
def sync_tree(platform_id):
    # task_logs.task_end(task_id, 'ok')
    print('platform_id:', platform_id)
    g.start_time = datetime.datetime.now()
    si, content, platform = get_connect(platform_id)
    sync_vcenter_tree(si, content, platform)


# @celery.task()
def sync_vcenter_vm(si, content, host, platform):
    # @celery.task()
    # def sync_vcenter_vm(host, platform):
    print ('sync_vm_start:', time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time())))
    vms = host.vm

    # print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))
    # 查询平台内所有的云主机列表
    # platform_vm_list = db_vm.vcenter_get_vm_by_platform_id(platform['id'], host.name)
    platform_vm_list = db.instances.vcenter_get_vm_by_platform_id(platform['id'], host.name)

    # instance = Instance(platform_id=platform['id'], si=si, content=content)

    vm_list = []
    for vm in platform_vm_list:
        vm_list.append(vm.uuid)
    # print(vm_list)
    for vm in vms:
        # print(dir(vm.config))

        # print(vm.summary.config.name)
        # print(vm.config.createDate)
        # return 'ccc'
        if vm.resourcePool:
            resource_pool_name = vm.resourcePool.name
            # db.instances.update_vm_rp_name_by_vm_mor_name(platform['id'], get_mor_name(vm), vm.resourcePool.name)
        else:
            resource_pool_name = None
        # 判断是否已存在云主机
        # print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))

        if vm.summary.guest != None:
            ip = vm.summary.guest.ipAddress
        else:
            ip = ''
        # print(vm_list)
        if vm.summary.config.uuid in vm_list:
            vm_list.remove(vm.summary.config.uuid)
            db.instances.vcenter_update_vm_by_uuid(uuid=vm.summary.config.uuid, platform_id=platform['id'],
                                                   vm_name=vm.summary.config.name,
                                                   vm_mor_name=get_mor_name(vm), template=vm.summary.config.template,
                                                   vm_path_name=vm.summary.config.vmPathName,
                                                   memory=vm.summary.config.memorySizeMB,
                                                   cpu=vm.summary.config.numCpu,
                                                   num_ethernet_cards=vm.summary.config.numEthernetCards,
                                                   num_virtual_disks=vm.summary.config.numVirtualDisks,
                                                   instance_uuid=vm.summary.config.instanceUuid,
                                                   guest_id=vm.summary.config.guestId,
                                                   guest_full_name=vm.summary.config.guestFullName,
                                                   host=host.name, ip=ip, status=vm.summary.runtime.powerState,
                                                   resource_pool_name=resource_pool_name)

        else:

            db.instances.vcenter_vm_create(uuid=vm.summary.config.uuid, platform_id=platform['id'],
                                           vm_name=vm.summary.config.name,
                                           vm_mor_name=get_mor_name(vm), template=vm.summary.config.template,
                                           vm_path_name=vm.summary.config.vmPathName,
                                           memory=vm.summary.config.memorySizeMB,
                                           cpu=vm.summary.config.numCpu,
                                           num_ethernet_cards=vm.summary.config.numEthernetCards,
                                           num_virtual_disks=vm.summary.config.numVirtualDisks,
                                           instance_uuid=vm.summary.config.instanceUuid,
                                           guest_id=vm.summary.config.guestId,
                                           guest_full_name=vm.summary.config.guestFullName,
                                           host=host.name, ip=ip, status=vm.summary.runtime.powerState,
                                           resource_pool_name=resource_pool_name, created_at=vm.config.createDate)

        # 同步 vm network device
        netowrk_device_manage.sync_network_device(platform_id=platform['id'], vm=vm)
        disk_manage.sync_disk(platform_id=platform['id'], vm=vm)

        # 异步处理 同步vm信息
        # sync_snapshot.apply_async(args=[platform["id"], vm.summary.config.uuid])
        sync_snapshot(platform_id=platform['id'], vm=vm)

        # print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))
        # 删除不存在的云主机
    if vm_list:
        for uuid in vm_list:
            # db_vm.vm_delete_by_uuid(platform['id'], host.name, uuid)
            db.instances.vm_delete_by_uuid(platform['id'], host.name, uuid)

            # 删除相关的 network disk
            db.network_devices.device_delete_by_vm_uuid(platform['id'], uuid)
            db.disks.device_delete_by_vm_uuid(platform['id'], uuid)
    print ('sync_vm_end:', time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time())))


def sync_vcenter_tree(si, content, platform):
    print ('sync_start:', time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time())))

    # 获取当前云平台的 tree_id
    # vcenter_ids = db_vcenter.vcenter_tree_get_all_id(platform['id'])
    vcenter_ids = db.vcenter.vcenter_tree_get_all_id(platform['id'])
    vcenter_list = []
    for tree in vcenter_ids:
        vcenter_list.append(tree.id)

    # 获取 platfrom tree

    result = db.vcenter.vcenter_tree_get_by_platform(platform['id'], platform['platform_name'], 1)
    if result:
        vcenter_list.remove(result.id)
        vCenter_pid = result.id

        db.vcenter.vcenter_tree_update(tree_type=1, platform_id=platform['id'], mor_name=None,
                                       name=platform['platform_name'])
    else:

        vCenter_pid = db.vcenter.vcenter_tree_create(tree_type=1, platform_id=platform['id'],
                                                     name=platform['platform_name'])
    datacenters = content.rootFolder.childEntity
    sync_datacenter(datacenters, si, content, platform, vcenter_list, vCenter_pid)

    print ('sync_end:', time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time())))
    # return True


# 同步datacenters
def sync_datacenter(datacenters, si, content, platform, vcenter_list, vCenter_pid):
    for dc in datacenters:
        # print('pid:', vCenter_pid)
        dc_mor = get_mor_name(dc)
        dc_host_moc = get_mor_name(dc.hostFolder)
        dc_vm_moc = get_mor_name(dc.vmFolder)

        # 同步vcenter port group
        netwroks = dc.network
        sync_network_port_group(netwroks, dc.name, dc_mor, platform['id'])

        # 同步datastore
        sync_datastore(platform, dc, si, content)
        # 异步处理 同步ds信息

        # sync_datastore.apply_async(args=[platform, dc, si])

        # 获取 dc tree
        # result = db_vcenter.vcenter_tree_get_by_dc(platform['id'], dc_mor, 2)
        result = db.vcenter.vcenter_tree_get_by_dc(platform['id'], dc_mor, 2)
        # print(22)
        if result:
            vcenter_list.remove(result.id)
            dc_pid = result.id
            db.vcenter.vcenter_tree_update(tree_type=2, platform_id=platform['id'], name=dc.name,
                                           dc_mor_name=dc_mor,
                                           dc_oc_name=dc.name, mor_name=dc_mor, dc_host_folder_mor_name=dc_host_moc,
                                           dc_vm_folder_mor_name=dc_vm_moc, pid=vCenter_pid)
        else:
            dc_pid = db.vcenter.vcenter_tree_create(tree_type=2, platform_id=platform['id'], name=dc.name,
                                                    dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=dc_mor,
                                                    dc_host_folder_mor_name=dc_host_moc,
                                                    dc_vm_folder_mor_name=dc_vm_moc, pid=vCenter_pid)
        # print(33)
        # print('dc_pid:', dc_pid)
        clusters = dc.hostFolder.childEntity
        # print(clusters.name)
        for cluster in clusters:
            # print(44)

            cluster_mor = get_mor_name(cluster)

            # 添加/更新 cluster 信息
            # 获取 cluster tree
            result = db.vcenter.vcenter_tree_get_by_cluster(platform['id'], cluster_mor, 3)

            if result:
                vcenter_list.remove(result.id)
                cluster_pid = result.id
                db.vcenter.vcenter_tree_update(tree_type=3, platform_id=platform['id'], name=cluster.name,
                                               dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=cluster_mor,
                                               dc_host_folder_mor_name=dc_host_moc, dc_vm_folder_mor_name=dc_vm_moc,
                                               cluster_mor_name=cluster_mor, cluster_oc_name=cluster.name,
                                               pid=dc_pid)
            else:

                cluster_pid = db.vcenter.vcenter_tree_create(tree_type=3, platform_id=platform['id'],
                                                             name=cluster.name,
                                                             dc_mor_name=dc_mor, dc_oc_name=dc.name,
                                                             mor_name=cluster_mor,
                                                             dc_host_folder_mor_name=dc_host_moc,
                                                             dc_vm_folder_mor_name=dc_vm_moc,
                                                             cluster_mor_name=cluster_mor,
                                                             cluster_oc_name=cluster.name, pid=dc_pid)

            rp_obj = content.viewManager.CreateContainerView(cluster, [vim.ResourcePool], True)
            rps = rp_obj.view

            for rp in rps:
                rp_mor = get_mor_name(rp)
                rp_info = db.vcenter.vcenter_tree_get_by_mor_name(platform['id'], rp_mor, 5)
                if rp_info:

                    vcenter_list.remove(rp_info.id)
                    if rp.parent.name == cluster.name:
                        db.vcenter.vcenter_tree_update(tree_type=5, platform_id=platform['id'], name=rp.name,
                                                       dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=rp_mor,
                                                       dc_host_folder_mor_name=dc_host_moc,
                                                       dc_vm_folder_mor_name=dc_vm_moc,
                                                       cluster_mor_name=cluster_mor,
                                                       cluster_oc_name=cluster.name, pid=cluster_pid)

                    else:
                        parent_rp_info = db.vcenter.vcenter_tree_get_by_mor_name(platform['id'],
                                                                                 get_mor_name(rp.parent), 5)
                        db.vcenter.vcenter_tree_update(tree_type=5, platform_id=platform['id'], name=rp.name,
                                                       dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=rp_mor,
                                                       dc_host_folder_mor_name=dc_host_moc,
                                                       dc_vm_folder_mor_name=dc_vm_moc,
                                                       cluster_mor_name=cluster_mor,
                                                       cluster_oc_name=cluster.name, pid=parent_rp_info.id)

                else:

                    if rp.parent.name == cluster.name:

                        db.vcenter.vcenter_tree_create(tree_type=5, platform_id=platform['id'], name=rp.name,
                                                       dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=rp_mor,
                                                       dc_host_folder_mor_name=dc_host_moc,
                                                       dc_vm_folder_mor_name=dc_vm_moc,
                                                       cluster_mor_name=cluster_mor,
                                                       cluster_oc_name=cluster.name, pid=cluster_pid)
                    else:

                        parent_rp_info = db.vcenter.vcenter_tree_get_by_mor_name(platform['id'],
                                                                                 get_mor_name(rp.parent), 5)

                        db.vcenter.vcenter_tree_create(tree_type=5, platform_id=platform['id'], name=rp.name,
                                                       dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=rp_mor,
                                                       dc_host_folder_mor_name=dc_host_moc,
                                                       dc_vm_folder_mor_name=dc_vm_moc,
                                                       cluster_mor_name=cluster_mor,
                                                       cluster_oc_name=cluster.name, pid=parent_rp_info.id)

            sync_resourcepool(platform, dc, cluster, si, content)
            # 异步处理 同步rp信息
            # sync_resourcepool.apply_async(args=[platform, dc, cluster, si, content])

            hosts = cluster.host
            for host in hosts:
                host_mor = get_mor_name(host)
                # 获取 host tree

                result = db.vcenter.vcenter_tree_get_by_mor_name(platform['id'], host_mor, 4)

                if result:
                    vcenter_list.remove(result.id)

                    db.vcenter.vcenter_tree_update(tree_type=4, platform_id=platform['id'], name=host.name,
                                                   dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=host_mor,
                                                   dc_host_folder_mor_name=dc_host_moc,
                                                   dc_vm_folder_mor_name=dc_vm_moc,
                                                   cluster_mor_name=cluster_mor, cluster_oc_name=cluster.name,
                                                   pid=cluster_pid)
                else:

                    db.vcenter.vcenter_tree_create(tree_type=4, platform_id=platform['id'], name=host.name,
                                                   dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=host_mor,
                                                   dc_host_folder_mor_name=dc_host_moc,
                                                   dc_vm_folder_mor_name=dc_vm_moc,
                                                   cluster_mor_name=cluster_mor, cluster_oc_name=cluster.name,
                                                   pid=cluster_pid)
                # 同步vm信息
                # 异步处理 同步vm信息
                sync_vcenter_vm(si, content, host, platform)
                # sync_vcenter_vm.apply_async(args=[si, content, host, platform])
                # sync_vcenter_vm.apply_async(args=[host, platform])

    # 删除未操作的 tree
    if vcenter_list:
        for id in vcenter_list:
            # db_vcenter.vcenter_tree_delete_by_id(id)
            db.vcenter.vcenter_tree_delete_by_id(id)


def vcenter_tree_list(platform_id):
    vcenter_tree = db.vcenter.vcenter_tree_list_by_platform_id(platform_id)

    vcenter_list = []
    if vcenter_tree:
        for tree in vcenter_tree:
            tree_tmp = dict()
            tree_tmp['id'] = tree.id
            tree_tmp['type'] = tree.type
            tree_tmp['platform_id'] = tree.platform_id
            tree_tmp['dc_host_folder_mor_name'] = tree.dc_host_folder_mor_name
            tree_tmp['dc_mor_name'] = tree.dc_mor_name
            tree_tmp['dc_oc_name'] = tree.dc_oc_name
            tree_tmp['dc_vm_folder_mor_name'] = tree.dc_vm_folder_mor_name
            tree_tmp['mor_name'] = tree.mor_name
            tree_tmp['name'] = tree.name
            tree_tmp['cluster_mor_name'] = tree.cluster_mor_name
            tree_tmp['cluster_oc_name'] = tree.cluster_oc_name
            tree_tmp['pid'] = tree.pid

            vcenter_list.append(tree_tmp)

    return vcenter_list
