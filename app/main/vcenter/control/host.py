# -*- coding:utf-8 -*-
import hashlib
import socket
import ssl
import time

from pyVim.task import WaitForTask
from pyVmomi import vim
from app.main.vcenter.control.utils import get_connect, get_obj_by_mor_name, get_obj, get_mor_name
from app.main.vcenter import db


class Host:
    def __init__(self, platform_id):
        self.si, self.content, self.platform = get_connect(platform_id)

    # 添加host
    def add_host(self, host_name, esxi_username, esxi_password, as_connected=True,
                 folder_name=None, cluster_id=None,
                 license_id=None, resource_pool=None,
                 fetch_ssl_thumbprint=None, esxi_ssl_thumbprint=None):
        """Add ESXi host to a cluster of folder in vCenter"""
        if db.host.get_host_by_name(host_name):
            raise ValueError('The host object already exists.')
        host_connect_spec = self.get_host_connect_spec(esxi_hostname=host_name, esxi_username=esxi_username,
                                                       esxi_password=esxi_password,
                                                       fetch_ssl_thumbprint=fetch_ssl_thumbprint,
                                                       esxi_ssl_thumbprint=esxi_ssl_thumbprint)
        if license_id:
            license = db.host.get_license_by_id(license_id)
            if license:
                license = license.licenseKey
        else:
            license = None
        task = None
        if folder_name:
            folder = self.search_folder(folder_name)  # 寻找文件夹
            try:
                # 构建任务
                task = folder.AddStandaloneHost(
                    spec=host_connect_spec, compResSpec=resource_pool,
                    addConnected=as_connected, license=license
                )
            except Exception as task_error:
                raise RuntimeError('Error adding host %s task' % task_error)
        elif cluster_id:
            cluster = db.vcenter.vcenter_tree_by_id(cluster_id)
            if cluster.type != 3:
                raise ValueError('The selected object is not a cluster')
            mor_name = cluster.mor_name
            cluster = get_obj_by_mor_name(self.content, [vim.ClusterComputeResource], mor_name)
            try:
                task = cluster.AddHost_Task(
                    spec=host_connect_spec, asConnected=as_connected,
                    resourcePool=resource_pool, license=license
                )
            except Exception as task_error:
                raise RuntimeError('Error adding host %s task' % task_error)
        try:
            WaitForTask(task)
        except Exception as task_error:
            raise Exception('Error adding host %s task' % task_error)
        # 同步
        new_host_id = self.sync_host(host_name)
        return new_host_id

    def sync_host(self, host_name):
        """
        TODO host.summary.quickStats数据不能直接获取，，全为0或-1，需要重新获取一次
        :param host_name:
        :return:
        """
        host = get_obj(self.content, [vim.HostSystem], host_name)
        capacity = 0
        free_capacity = 0
        for ds in host.datastore:
            capacity += ds.summary.capacity
            free_capacity += ds.summary.freeSpace
        used_capacity = capacity - free_capacity
        config = host.summary.config
        runtime = host.summary.runtime
        # print config
        data = dict(name=config.name, mor_mame=get_mor_name(host.summary.host), port=config.port,
                    power_state=str(runtime.powerState), connection_state=str(runtime.connectionState),
                    maintenance_mode=runtime.inMaintenanceMode, platform_id=self.platform['id'],
                    uuid=host.summary.hardware.uuid, cpu_cores=int(host.summary.hardware.numCpuCores),
                    memory=host.summary.hardware.memorySize, used_memory=host.summary.quickStats.overallMemoryUsage,
                    capacity=capacity, used_capacity=used_capacity, used_cpu=host.summary.quickStats.overallCpuUsage,
                    cpu_mhz=host.summary.hardware.cpuMhz, cpu_model=host.summary.hardware.cpuModel,
                    version=config.product.version, image=config.product.name, build=config.product.build,
                    full_name=config.product.fullName, boot_time=runtime.bootTime,
                    uptime=host.summary.quickStats.uptime, vm_nums=len(host.vm), network_nums=len(host.network))
        new_host_id = db.host.add_host(**data)
        return new_host_id

    # 连接host
    def get_host_connect_spec(self, esxi_hostname, esxi_username, esxi_password,
                              fetch_ssl_thumbprint=None, esxi_ssl_thumbprint=True,
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

    # 寻找存储文件夹
    def search_folder(self, folder_name):
        """
            Search folder in vCenter
            Returns: folder object
        """
        search_index = self.content.searchIndex
        folder_obj = search_index.FindByInventoryPath(folder_name)
        if not (folder_obj and isinstance(folder_obj, vim.Folder)):
            raise ValueError('The specified file was not found')
        return folder_obj

    # 移除host
    def remove_host(self, host_id):
        """Remove host from vCenter"""
        host = db.host.get_host_by_id(host_id)
        task = None
        host_object = get_obj(self.content, [vim.HostSystem], host.name)
        # Check parent type
        parent_type = self.get_parent_type(host_object)
        try:
            if parent_type == 'folder':
                task = host_object.Destroy_Task()
            elif parent_type == parent_type == 'cluster':
                if not host_object.runtime.inMaintenanceMode:
                    raise Exception('Host not in maintenance mode.')
                task = host_object.Destroy_Task()
        except Exception as e:
            raise RuntimeError('Build task error.')
        try:
            WaitForTask(task)
            db.host.del_host(host.name)
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

    # （维护）模式更新（暂时未使用）
    def put_host_in_maintenance_mode(self, host_object):
        """Put host in maintenance mode, if not already"""
        if not host_object.runtime.inMaintenanceMode:
            try:
                try:
                    maintenance_mode_task = host_object.EnterMaintenanceMode_Task(300, True, None)
                except vim.fault.InvalidState as invalid_state:
                    raise Exception('Error')
                except vim.fault.Timedout as timed_out:
                    raise Exception('Error')

                except vim.fault.Timedout as timed_out:
                    raise Exception('Error')
                WaitForTask(maintenance_mode_task)
            except TaskError as task_err:
                raise Exception('Error')

    # 同步需要
    def sync_licenses(self):
        licenses = self.si.content.licenseManager.licenses
        for license in licenses:
            data = dict(
                name=license.name,
                license_key=license.licenseKey,
                edition_key=license.editionKey,
                used=license.used,
                total=license.total,
            )
            db.host.create_license(**data)


def get_host_all(platform_id):
    hosts = db.host.get_host_all(platform_id)
    host_list = []
    for host in hosts:
        data = dict(
            id=host.id, name=host.name, mor_mame=host.mor_name, port=host.port,
            power_state=host.power_state, connection_state=host.connection_state,
            maintenance_mode=host.maintenance_mode, platform_id=platform_id,
            uuid=host.uuid, cpu_cores=host.cpu_cores,  ram=host.ram, used_ram=host.used_ram,
            capacity=host.capacity, free_capacity=host.free_capacity, used_cpu=host.used_cpu,
            cpu_mhz=host.cpu_mhz, cpu_model=host.cpu_model,
            version=host.version, image=host.image, build=host.build,
            full_name=host.full_name, boot_time=str(host.boot_time), uptime=host.uptime
        )
        host_list.append(data)
    return host_list
