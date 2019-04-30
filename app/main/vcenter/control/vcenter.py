# -*- coding:utf-8 -*-
from app.main.vcenter.control import get_mor_name, connect_server, get_connect
from app.main.vcenter.control.network_port_group import sync_network_port_group
from app.main.vcenter.control import network_devices as netowrk_device_manage
from app.main.vcenter.control import disks as disk_manage
from app.main.vcenter import db

from pyVim import connect
import atexit
import time
# import threadpool
import threading


from pyVmomi import vmodl
from pyVmomi import vim

from app.exts import celery


@celery.task()
def sync_tree(platform_id):
    si, content, platform = get_connect(platform_id)
    sync_vcenter_tree(si, content, platform)


def sync_vcenter_vm(si, content, host, platform):
    vms = host.vm

    # print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))
    # 查询平台内所有的云主机列表
    # platform_vm_list = db_vm.vcenter_get_vm_by_platform_id(platform['id'], host.name)
    platform_vm_list = db.instances.vcenter_get_vm_by_platform_id(platform['id'], host.name)

    # instance = Instance(platform_id=platform['id'], si=si, content=content)

    vm_list = []
    for vm in platform_vm_list:
        vm_list.append(vm.uuid)

    for vm in vms:

        # 判断是否已存在云主机
        # print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))

        if vm.summary.guest != None:
            ip = vm.summary.guest.ipAddress
        else:
            ip = ''

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
                                                   host=host.name, ip=ip, status=vm.summary.runtime.powerState)

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
                                           host=host.name, ip=ip, status=vm.summary.runtime.powerState)

        # 同步 vm network device
        netowrk_device_manage.sync_network_device(platform_id=platform['id'], vm=vm)
        disk_manage.sync_disk(platform_id=platform['id'], vm=vm)

    # print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))
    # 删除不存在的云主机
    if vm_list:
        for uuid in vm_list:
            # db_vm.vm_delete_by_uuid(platform['id'], host.name, uuid)
            db.instances.vm_delete_by_uuid(platform['id'], host.name, uuid)

            # 删除相关的 network disk
            db.network_devices.device_delete_by_vm_uuid(platform['id'], uuid)
            db.disks.device_delete_by_vm_uuid(platform['id'], uuid)


def sync_vcenter_tree(si, content, platform):
    print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))

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

        db.vcenter.vcenter_tree_update(tree_type=1, platform_id=platform['id'], mor_name=None,
                                       name=platform['platform_name'])
    else:

        db.vcenter.vcenter_tree_create(tree_type=1, platform_id=platform['id'], name=platform['platform_name'])
    datacenters = content.rootFolder.childEntity
    for dc in datacenters:

        dc_mor = get_mor_name(dc)
        dc_host_moc = get_mor_name(dc.hostFolder)
        dc_vm_moc = get_mor_name(dc.vmFolder)

        # 同步vcenter port group
        netwroks = dc.network
        # sync_vcenter_network(netwroks, dc.name, dc_mor, platform['id'])

        sync_network_port_group(netwroks, dc.name, dc_mor, platform['id'])

        # 获取 dc tree
        # result = db_vcenter.vcenter_tree_get_by_dc(platform['id'], dc_mor, 2)
        result = db.vcenter.vcenter_tree_get_by_dc(platform['id'], dc_mor, 2)

        if result:
            vcenter_list.remove(result.id)
            db.vcenter.vcenter_tree_update(tree_type=2, platform_id=platform['id'], name=dc.name, dc_mor_name=dc_mor,
                                           dc_oc_name=dc.name, mor_name=dc_mor, dc_host_folder_mor_name=dc_host_moc,
                                           dc_vm_folder_mor_name=dc_vm_moc)
        else:
            db.vcenter.vcenter_tree_create(tree_type=2, platform_id=platform['id'], name=dc.name, dc_mor_name=dc_mor,
                                           dc_oc_name=dc.name, mor_name=dc_mor, dc_host_folder_mor_name=dc_host_moc,
                                           dc_vm_folder_mor_name=dc_vm_moc)

        clusters = dc.hostFolder.childEntity
        # print(clusters.name)
        for cluster in clusters:

            resourcePool_mor = get_mor_name(cluster.resourcePool)

            cluster_mor = get_mor_name(cluster)

            # 添加/更新 cluster 信息
            # 获取 cluster tree
            result = db.vcenter.vcenter_tree_get_by_cluster(platform['id'], cluster_mor, 3)

            if result:
                vcenter_list.remove(result.id)

                db.vcenter.vcenter_tree_update(tree_type=3, platform_id=platform['id'], name=cluster.name,
                                               dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=cluster_mor,
                                               dc_host_folder_mor_name=dc_host_moc, dc_vm_folder_mor_name=dc_vm_moc,
                                               cluster_mor_name=cluster_mor, cluster_oc_name=cluster.name, )
            else:

                db.vcenter.vcenter_tree_create(tree_type=3, platform_id=platform['id'], name=cluster.name,
                                               dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=cluster_mor,
                                               dc_host_folder_mor_name=dc_host_moc, dc_vm_folder_mor_name=dc_vm_moc,
                                               cluster_mor_name=cluster_mor, cluster_oc_name=cluster.name, )

            hosts = cluster.host
            for host in hosts:
                host_mor = get_mor_name(host)
                # 获取 host tree

                result = db.vcenter.vcenter_tree_get_by_cluster(platform['id'], host_mor, 4)

                if result:
                    vcenter_list.remove(result.id)

                    db.vcenter.vcenter_tree_update(tree_type=4, platform_id=platform['id'], name=host.name,
                                                   dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=host_mor,
                                                   dc_host_folder_mor_name=dc_host_moc, dc_vm_folder_mor_name=dc_vm_moc,
                                                   cluster_mor_name=cluster_mor, cluster_oc_name=cluster.name)
                else:

                    db.vcenter.vcenter_tree_create(tree_type=4, platform_id=platform['id'], name=host.name,
                                                   dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=host_mor,
                                                   dc_host_folder_mor_name=dc_host_moc, dc_vm_folder_mor_name=dc_vm_moc,
                                                   cluster_mor_name=cluster_mor, cluster_oc_name=cluster.name)
                # 同步vm信息
                sync_vcenter_vm(si, content, host, platform)

    # 删除未操作的 tree
    if vcenter_list:
        for id in vcenter_list:
            # db_vcenter.vcenter_tree_delete_by_id(id)
            db.vcenter.vcenter_tree_delete_by_id(id)

    # print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))
    # return True


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

            vcenter_list.append(tree_tmp)

    return vcenter_list
