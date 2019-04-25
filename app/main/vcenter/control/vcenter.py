# -*- coding:utf-8 -*-
from app.main.vcenter.control import get_mor_name
from app.main.vcenter.db import vcenter as db_vcenter
from app.main.vcenter.db import instances as db_vm
from app.main.vcenter.db import network_port_group as db_network
from app.main.vcenter.control import network_devices as netowrk_device_manage
from pyVim import connect
import atexit
import time
# import threadpool
import threading

# from pyVmomi import vmodl
from pyVmomi import vim
from app.main.base.control import cloud_platform


def connect_server(host, user, password, port, ssl=True):
    # print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))
    if ssl:
        service_instance = connect.SmartConnectNoSSL(host=host,
                                                     user=user,
                                                     pwd=password,
                                                     port=int(port))
    else:
        service_instance = connect.SmartConnect(host=host,
                                                user=user,
                                                pwd=password,
                                                port=int(port))
    return service_instance


def get_connect(platform_id):
    options = {
        'id': platform_id
    }
    platforms = cloud_platform.platform_list(options)
    if platforms:
        platform = platforms[0]
        s = connect_server(platform['ip'], platform['name'], platform['password'], platform['port'])
        atexit.register(connect.Disconnect, s)
    else:
        raise Exception('unable to find platform')
    content = s.RetrieveContent()
    return s, content, platforms[0]


def sync_tree(platform_id):
    s, content, platform = get_connect(platform_id)
    sync_vcenter_tree(content, platform)


def sync_vcenter_network(netwroks, dc_name, dc_mor_name, platform_id):
    # print('dc_name:', dc_name)
    # print('dc_mor_name:', dc_mor_name)
    # print('platform_id:', platform_id)
    if netwroks:
        for network in netwroks:
            pass
            # 判断是否存在网络
            network_mor_name = get_mor_name(network)
            network_info = db_network.network_list_by_mor_name(platform_id, network_mor_name)
            if not network_info:
                db_network.network_create(network.name, network_mor_name, dc_name, dc_mor_name, platform_id)
            else:
                db_network.network_update(network_info.get('id'), network.name, network_mor_name, dc_name, dc_mor_name)


def sync_vcenter_vm(host, platform):
    vms = host.vm

    # print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))
    # 查询平台内所有的云主机列表
    platform_vm_list = db_vm.vcenter_get_vm_by_platform_id(platform['id'], host.name)

    vm_list = []
    for vm in platform_vm_list:
        vm_list.append(vm.uuid)

    for vm in vms:
        #
        # print('power:', vm.summary.runtime.powerState)

        # 判断是否已存在云主机
        # print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))

        if vm.summary.guest != None:
            ip = vm.summary.guest.ipAddress
        else:
            ip = ''

        if vm.summary.config.uuid in vm_list:
            vm_list.remove(vm.summary.config.uuid)
            # print(vm.summary.config)
            db_vm.vcenter_update_vm_by_uuid(uuid=vm.summary.config.uuid, platform_id=platform['id'],
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

        else:
            db_vm.vcenter_vm_create(uuid=vm.summary.config.uuid, platform_id=platform['id'],
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

        # print('vm_list:', vm_list)

    # print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))
    # 删除不存在的云主机
    if vm_list:
        for uuid in vm_list:
            db_vm.vm_delete_by_uuid(platform['id'], host.name, uuid)


def sync_vcenter_tree(content, platform):
    print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))

    # 获取当前云平台的 tree_id
    vcenter_ids = db_vcenter.vcenter_tree_get_all_id(platform['id'])
    vcenter_list = []
    for tree in vcenter_ids:
        vcenter_list.append(tree.id)

    # 获取 platfrom tree
    result = db_vcenter.vcenter_tree_get_by_platform(platform['id'], platform['platform_name'], 1)
    if result:
        vcenter_list.remove(result.id)
        # db_vcenter.vcenter_tree_update()
        db_vcenter.vcenter_tree_update(tree_type=1, platform_id=platform['id'], mor_name=None,
                                       name=platform['platform_name'])
    else:
        db_vcenter.vcenter_tree_create(tree_type=1, platform_id=platform['id'], name=platform['platform_name'])
    datacenters = content.rootFolder.childEntity
    for dc in datacenters:

        netwroks = dc.network

        dc_mor = get_mor_name(dc)
        dc_host_moc = get_mor_name(dc.hostFolder)
        dc_vm_moc = get_mor_name(dc.vmFolder)

        # 同步vcenter网络
        # print('cccc')
        # sync_network_thread = threading.Thread(target=sync_vcenter_network,
        #                                        args=(netwroks, dc.name, dc_mor, platform['id']))
        # sync_network_thread.start()
        # return True
        sync_vcenter_network(netwroks, dc.name, dc_mor, platform['id'])

        # 获取 dc tree
        result = db_vcenter.vcenter_tree_get_by_dc(platform['id'], dc_mor, 2)

        if result:
            vcenter_list.remove(result.id)
            db_vcenter.vcenter_tree_update(tree_type=2, platform_id=platform['id'], name=dc.name, dc_mor_name=dc_mor,
                                           dc_oc_name=dc.name, mor_name=dc_mor, dc_host_folder_mor_name=dc_host_moc,
                                           dc_vm_folder_mor_name=dc_vm_moc)
        else:
            db_vcenter.vcenter_tree_create(tree_type=2, platform_id=platform['id'], name=dc.name, dc_mor_name=dc_mor,
                                           dc_oc_name=dc.name, mor_name=dc_mor, dc_host_folder_mor_name=dc_host_moc,
                                           dc_vm_folder_mor_name=dc_vm_moc)

        clusters = dc.hostFolder.childEntity
        # print(clusters.name)
        for cluster in clusters:
            # print('cluster.Folder', cluster.vmFolder)
            # resourcePool = '%s' % cluster.resourcePool
            # resourcePool_mor = resourcePool.replace("'", "").split(':', 1)[1]

            resourcePool_mor = get_mor_name(cluster.resourcePool)

            cluster_mor = get_mor_name(cluster)

            # 添加/更新 cluster 信息
            # 获取 cluster tree
            result = db_vcenter.vcenter_tree_get_by_cluster(platform['id'], cluster_mor, 3)

            if result:
                vcenter_list.remove(result.id)
                db_vcenter.vcenter_tree_update(tree_type=3, platform_id=platform['id'], name=cluster.name,
                                               dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=cluster_mor,
                                               dc_host_folder_mor_name=dc_host_moc, dc_vm_folder_mor_name=dc_vm_moc,
                                               cluster_mor_name=cluster_mor, cluster_oc_name=cluster.name, )
            else:

                db_vcenter.vcenter_tree_create(tree_type=3, platform_id=platform['id'], name=cluster.name,
                                               dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=cluster_mor,
                                               dc_host_folder_mor_name=dc_host_moc, dc_vm_folder_mor_name=dc_vm_moc,
                                               cluster_mor_name=cluster_mor, cluster_oc_name=cluster.name, )

            hosts = cluster.host
            for host in hosts:
                host_mor = get_mor_name(host)
                # 获取 host tree
                result = db_vcenter.vcenter_tree_get_by_cluster(platform['id'], host_mor, 4)

                if result:
                    vcenter_list.remove(result.id)
                    db_vcenter.vcenter_tree_update(tree_type=4, platform_id=platform['id'], name=host.name,
                                                   dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=host_mor,
                                                   dc_host_folder_mor_name=dc_host_moc, dc_vm_folder_mor_name=dc_vm_moc,
                                                   cluster_mor_name=cluster_mor, cluster_oc_name=cluster.name)
                else:
                    # db_vcenter.vcenter_tree_create(options)
                    db_vcenter.vcenter_tree_create(tree_type=4, platform_id=platform['id'], name=host.name,
                                                   dc_mor_name=dc_mor, dc_oc_name=dc.name, mor_name=host_mor,
                                                   dc_host_folder_mor_name=dc_host_moc, dc_vm_folder_mor_name=dc_vm_moc,
                                                   cluster_mor_name=cluster_mor, cluster_oc_name=cluster.name)
                # 同步vm信息

                sync_vcenter_vm(host, platform)

                # sync_vm_thread = threading.Thread(target=sync_vcenter_vm, args=(host, platform))
                # sync_vm_thread.start()

                # for vm in vms:

                #     # print(vm)
                #     # vm_info = '%s' % vm
                #     # vm_mor = vm_info.replace("'", "").split(':', 1)[1]
                #     pass
                #     # vm_mor = get_mor_name(vm)
                #
                #     # print('        vm_mor:', vm_mor)
                #     # print('        vm:', vm.summary.config.name)
    # print(vcenter_list)
    # 删除未操作的 tree
    if vcenter_list:
        for id in vcenter_list:
            db_vcenter.vcenter_tree_delete_by_id(id)

    print time.strftime('%Y.%m.%d:%H:%M:%S', time.localtime(time.time()))
    return True


def vcenter_tree_list(platform_id):
    vcenter_tree = db_vcenter.vcenter_tree_list_by_platform_id(platform_id)
    # print(vcenter_tree)
    vcenter_list = []
    if vcenter_tree:

        for tree in vcenter_tree:
            # print(tree)
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
