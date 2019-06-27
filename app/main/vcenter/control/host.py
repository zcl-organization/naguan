# -*- coding:utf-8 -*-
import datetime
import hashlib
import socket
import ssl

from pyVim.task import WaitForTask
from pyVmomi import vim

from app.main.vcenter.control.utils import get_obj_by_mor_name, get_obj, get_mor_name
from app.main.vcenter import db
from app.main.vcenter.utils.base import VCenter


def sync_host(vcenter_obj, cluster_obj, host_obj):
    host_mor_name = get_mor_name(host_obj)
    cluster_mor_name = get_mor_name(cluster_obj)
    # 获取本地tree_cluster对象
    tree_cluster = db.vcenter.vcenter_tree_get_by_mor_name(vcenter_obj.platform['id'], cluster_mor_name, 3)
    # 获取本地tree_host对象
    tree_host_info = db.vcenter.vcenter_tree_get_by_mor_name(vcenter_obj.platform['id'], host_mor_name, 4)
    if tree_host_info:
        host_tree = db.vcenter.vcenter_tree_update(tree_type=4, platform_id=vcenter_obj.platform['id'],
                                                   name=host_obj.name, dc_mor_name=tree_cluster.dc_mor_name,
                                                   dc_oc_name=tree_cluster.dc_oc_name, mor_name=host_mor_name,
                                                   dc_host_folder_mor_name=tree_cluster.dc_host_folder_mor_name,
                                                   dc_vm_folder_mor_name=tree_cluster.dc_vm_folder_mor_name,
                                                   cluster_mor_name=cluster_mor_name,
                                                   cluster_oc_name=cluster_obj.name,
                                                   pid=tree_cluster.id)
    else:
        host_tree = db.vcenter.vcenter_tree_create(tree_type=4, platform_id=vcenter_obj.platform['id'],
                                                   name=host_obj.name, dc_mor_name=tree_cluster.dc_mor_name,
                                                   dc_oc_name=tree_cluster.dc_oc_name, mor_name=host_mor_name,
                                                   dc_host_folder_mor_name=tree_cluster.dc_host_folder_mor_name,
                                                   dc_vm_folder_mor_name=tree_cluster.dc_vm_folder_mor_name,
                                                   cluster_mor_name=cluster_mor_name,
                                                   cluster_oc_name=cluster_obj.name,
                                                   pid=tree_cluster.id)
    host_local = sync_host_local(vcenter_obj.platform['id'], host_obj, tree_cluster)
    return host_tree, host_local


# host表同步
def sync_host_local(platform_id, host_obj, tree_cluster):
    """
    新连接的host，host.summary.quickStats数据不能直接获取，，全为0或-1，需要重新获取一次
    """
    host = host_obj
    capacity = 0
    free_capacity = 0
    for ds in host.datastore:
        capacity += ds.summary.capacity
        free_capacity += ds.summary.freeSpace
    used_capacity = capacity - free_capacity
    config = host.summary.config
    runtime = host.summary.runtime
    # print config
    data = dict(name=config.name, mor_mame=get_mor_name(host), dc_name=tree_cluster.dc_oc_name,
                dc_mor_name=tree_cluster.dc_mor_name, cluster_name=tree_cluster.cluster_oc_name,
                cluster_mor_name=tree_cluster.cluster_mor_name, port=config.port,
                power_state=str(runtime.powerState), connection_state=str(runtime.connectionState),
                maintenance_mode=runtime.inMaintenanceMode, platform_id=platform_id,
                uuid=host.summary.hardware.uuid, cpu_cores=int(host.summary.hardware.numCpuCores),
                memory=host.summary.hardware.memorySize, used_memory=host.summary.quickStats.overallMemoryUsage,
                capacity=capacity, used_capacity=used_capacity, used_cpu=host.summary.quickStats.overallCpuUsage,
                cpu_mhz=host.summary.hardware.cpuMhz, cpu_model=host.summary.hardware.cpuModel,
                version=config.product.version, image=config.product.name, build=config.product.build,
                full_name=config.product.fullName, boot_time=runtime.bootTime.strftime('%Y-%m-%d %H:%M:%S'),
                uptime=host.summary.quickStats.uptime, vm_nums=len(host.vm), network_nums=len(host.network))
    # 获取本地cluster对象
    cluster_info = db.host.get_host_by_name(platform_id, config.name)
    if cluster_info:
        host_local = db.host.update_host(**data)
    else:
        host_local = db.host.add_host(**data)
    return host_local


class Host:
    def __init__(self, platform_id):
        self._platform_id = platform_id
        self._vCenter = VCenter(platform_id)

    # 添加host
    def add_host(self, host_name, esxi_username, esxi_password, as_connected=True, cluster_id=None,
                 license_id=None, resource_pool=None):
        """Add ESXi host to a cluster of folder in vCenter"""
        if db.host.get_host_by_name(self._platform_id, host_name):
            raise ValueError('The host object already exists.')
        host_connect_spec = self.get_host_connect_spec(esxi_hostname=host_name, esxi_username=esxi_username,
                                                       esxi_password=esxi_password)
        if license_id:
            license = db.license.get_license_by_id(license_id)
            if license:
                license = license.licenseKey
        else:
            license = None
        cluster = db.clusters.get_cluster(self._platform_id, cluster_id)
        vcenter_tree_cluster = db.vcenter.get_vcenter_obj_by_mor_name(self._platform_id, cluster.mor_name)
        if vcenter_tree_cluster.type != 3:
            raise ValueError('The selected object is not a cluster')
        cluster_obj = get_obj_by_mor_name(self._vCenter.connect, [vim.ClusterComputeResource], cluster.mor_name)
        try:
            task = cluster_obj.AddHost_Task(
                spec=host_connect_spec, asConnected=as_connected,
                resourcePool=resource_pool, license=license
            )
            WaitForTask(task)
        except Exception as task_error:
            raise Exception('Error adding host %s task' % task_error)
        # 同步
        host = get_obj(self._vCenter.connect, [vim.HostSystem], host_name)
        host_tree, host_local = sync_host(vcenter_obj=self._vCenter, cluster_obj=cluster_obj, host_obj=host)
        return host_local

    # 获取host配置
    def get_host_connect_spec(self, esxi_hostname, esxi_username, esxi_password,
                              fetch_ssl_thumbprint=None, esxi_ssl_thumbprint=None,
                              force_connection=True):
        """
        Returns: host connection specification
        """
        host_connect_spec = vim.host.ConnectSpec()
        host_connect_spec.hostName = esxi_hostname
        host_connect_spec.userName = esxi_username
        host_connect_spec.password = esxi_password
        host_connect_spec.force = force_connection
        # Get the thumbprint of the SSL certificate
        if fetch_ssl_thumbprint and esxi_ssl_thumbprint == '':
            # We need to grab the thumbprint manually because it's not included in
            # the task error via an SSLVerifyFault exception anymore
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            wrapped_socket = ssl.wrap_socket(sock)
            try:
                wrapped_socket.connect((esxi_hostname, 443))
            except socket.error as socket_error:
                return "Cannot connect to host : %s" % socket_error
            else:
                der_cert_bin = wrapped_socket.getpeercert(True)
                # thumb_md5 = hashlib.md5(der_cert_bin).hexdigest()
                thumb_sha1 = self.format_number(hashlib.sha1(der_cert_bin).hexdigest())
                # thumb_sha256 = hashlib.sha256(der_cert_bin).hexdigest()
            wrapped_socket.close()
            host_connect_spec.sslThumbprint = thumb_sha1
        else:
            host_connect_spec.sslThumbprint = esxi_ssl_thumbprint
        return host_connect_spec

    @staticmethod
    def format_number(number):
        """Format number"""
        string = str(number)
        return ':'.join(a + b for a, b in zip(string[::2], string[1::2]))

    # 移除host
    def remove_host(self, host_id):
        """Remove host from vCenter"""
        host = db.host.get_host_by_id(host_id)
        task = None
        host_object = get_obj(self._vCenter.connect, [vim.HostSystem], host.name)
        # Check parent type
        parent_type = self.get_parent_type(host_object)
        try:
            if parent_type == 'folder':
                task = host_object.Destroy_Task()
            elif parent_type == 'cluster':
                if not host_object.runtime.inMaintenanceMode:
                    raise Exception('Host not in maintenance mode.')
                task = host_object.Destroy_Task()
        except Exception as e:
            raise RuntimeError('Build task error.')
        try:
            WaitForTask(task)
            db.host.del_host_by_id(host_id)
            db.vcenter.vcenter_tree_del_by_mor_name(self._platform_id, host.mor_name)
        except Exception as e:
            raise Exception('Error removing host %s task.' % e)

    # 查询父类类型
    def get_parent_type(self, host_object):
        """
            Get the type of the parent object
            Returns: string with 'folder' or 'cluster'
        """
        object_type = None
        # check 'vim.ClusterComputeResource' first because it's also an
        # instance of 'vim.ComputeResource'
        if isinstance(host_object.parent, vim.ClusterComputeResource):
            object_type = 'cluster'
        elif isinstance(host_object.parent, vim.ComputeResource):
            object_type = 'folder'
        return object_type

    # （维护）模式更新
    def put_host_in_maintenance_mode(self, host_id):
        """Put host in maintenance mode, if not already"""
        host = db.host.get_host_by_id(host_id)
        if not host:
            raise ValueError('The host id does not exist')
        host_object = get_obj(self._vCenter.connect, [vim.HostSystem], host.name)
        if not host_object.runtime.inMaintenanceMode:  # ExitMaintenanceMode_Task
            try:
                # EnterMaintenanceMode_Task 三个参数，
                # timeout，当主机成功进入维护模式或超时过期时，任务完成，在后一种情况下，任务包含超时错误。如果超时小于或等于零，则不存在超时。超时以秒为单位指定
                # evacuatePoweredOffVms，这是一个只有VirtualCenter支持的参数。如果设置为true，对于已禁用DRS的集群，除非手动重新注册所有已关闭电源的虚拟机，
                # 否则任务不会成功;对于启用DRS的集群，VirtualCenter将自动重新注册关闭电源的虚拟机，关闭电源的虚拟机可能只保留在主机上，
                # 有原因两个:(1)没有找到用于重新注册的兼容主机;(2)虚拟机禁用DRS。如果设置为false，则不需要移动关闭电源的虚拟机
                # maintenanceSpec 主机进入维护模式时要采取的任何其他操作。如果省略，默认操作将在HostMaintenanceSpec中记录下来

                maintenance_mode_task = host_object.EnterMaintenanceMode_Task(300, True, None)
                WaitForTask(maintenance_mode_task)
                mode = True
            except Exception as e:
                raise Exception('Error entering maintenance mode')
        else:
            try:
                maintenance_mode_task = host_object.ExitMaintenanceMode_Task(0)
                WaitForTask(maintenance_mode_task)
                mode = False
            except Exception as e:
                raise Exception('Error exit maintenance mode')
        db.host.put_host_maintenance_mode(host_id, mode)
        return mode

    def find_host(self, id=None, host_name=None, dc_name=None, cluster_name=None):
        hosts = db.host.find_host(self._platform_id, id, host_name, dc_name, cluster_name)
        host_list = []
        for host in hosts:
            data = dict(
                id=host.id, name=host.name, mor_mame=host.mor_name, dc_name=host.dc_name,
                dc_mor_name=host.dc_mor_name, cluster_name=host.cluster_name,
                cluster_mor_name=host.cluster_mor_name, port=host.port,
                power_state=host.power_state, connection_state=host.connection_state,
                maintenance_mode=host.maintenance_mode, platform_id=self._platform_id,
                uuid=host.uuid, cpu_cores=host.cpu_cores,  cpu_mhz=host.cpu_mhz, used_cpu=host.used_cpu,
                memory=host.memory, used_memory=host.used_memory, capacity=host.capacity,
                used_capacity=host.used_capacity, cpu_model=host.cpu_model,
                version=host.version, image=host.image, build=host.build,
                full_name=host.full_name, boot_time=str(host.boot_time), uptime=host.uptime,
                vm_nums=host.vm_nums, network_nums=host.network_nums,
            )
            host_list.append(data)
        return host_list
