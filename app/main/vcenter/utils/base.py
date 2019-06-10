# -*- coding: utf-8 -*-
import atexit
from pyVim import connect
from pyVmomi import vim

from app.main.base.control import cloud_platform
from app.main.vcenter.control.utils import connect_server


class signleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(signleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class VCenter(signleton):
    def __init__(self, platform_id):
        platform_info = cloud_platform.platform_by_id(platform_id)
        if not platform_info:
            # TODO 考虑一次同步
            raise RuntimeError("No Find Platform")
        
        self._platform = platform_info
        self._server_instance = self._connect_server(platform_info)
        atexit.register(connect.Disconnect, self._server_instance)
        self._connect = self._server_instance.RetrieveContent()
    
    def _connect_server(self, platform_info):
        return connect_server(
            host=platform_info['ip'], 
            user=platform_info['name'], 
            password=platform_info['password'], 
            port=platform_info['port']
        )
    
    def get_si(self):
        return self._server_instance

    def get_connect(self):
        return self._connect

    def get_platform(self):
        return self._platform

    @property
    def si(self):
        return self.get_si()

    @property
    def connect(self):
        return self.get_connect()

    @property
    def platform(self):
        self.get_platform()

    def find_hostsystem_by_name(self, host_name):
        return self._get_object([vim.HostSystem], host_name)

    def find_datacenter_by_name(self, dc_name):
        return self._get_object([vim.Datacenter], dc_name)
    
    def find_datastore_by_name(self, ds_name):
        return self._get_object([vim.Datastore], ds_name)

    def find_cluster_by_name(self, cluster_name):
        return self._get_object([vim.ClusterComputeResource], cluster_name)
    
    def _get_object(self, vim_type, name, folder=None):
        if not folder:
            folder = self._connect.rootFolder

        container = self._connect.viewManager.CreateContainerView(folder, vim_type, True)
        for managed_object_ref in container.view:
            if managed_object_ref.name == name:
                return managed_object_ref

        return None
