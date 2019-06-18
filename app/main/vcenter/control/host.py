# -*- coding:utf-8 -*-
import hashlib
import socket
import ssl
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
        # try:
        #     WaitForTask(task)
        # except Exception as task_error:
        #     raise Exception('Error adding host %s task' % task_error)
        # 同步
        host = get_obj(self.content, [vim.HostSystem], host_name)
        self.sync_host(host)

    def sync_host(self, host):
        config = host.summary.config
        runtime = host.summary.runtime
        data = dict(name=config.name, mor_mame=get_mor_name(host.summary.host), port=config.port,
                    power_state=runtime.powerState, maintenance_mode=runtime.inMaintenanceMode,
                    platform_id=self.platform['id'], uuid=host.summary.hardware.uuid, cpu=None, ram=None, used_ram=None,
                    rom=None, used_rom=None, cpu_model=host.summary.hardware.cpuModel, version=config.prodect.version,
                    image=config.prodect.name, build=config.prodect.build, full_name=config.prodect.fullName,
                    boot_time=runtime.bootTime, uptime=host.summary.quickStats)
        import pdb
        pdb.set_trace()

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
    def remove_host(self, host_name):
        """Remove host from vCenter"""
        task = None
        host_object = get_obj(self.content, [vim.HostSystem], host_name)
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
        except Exception as e:
            raise Exception('Error removing host %s task.' % e)

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

    # 模式更新
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
                wait_for_task(maintenance_mode_task)
            except TaskError as task_err:
                raise Exception('Error')

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
