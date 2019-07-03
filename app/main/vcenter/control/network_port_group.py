# -*- coding:utf-8 -*-
from pyVmomi import vim

from flask import g

from app.main.vcenter.control.utils import get_obj, get_mor_name, get_connect
# from app.main.vcenter.control.vcenter import get_connect as pg_get_connect
from app.main.vcenter import db
from app.main.vcenter.utils.vm_port_group_manager import VMPortGroupManager, VMDvsPortGroupManager


# def sync_network_port_group(netwroks, dc_name, dc_mor_name, platform_id):
def sync_network_port_group(netwrok_datas, platform_id):
    """
    同步一组端口组信息
    TODO 问题在于同步时数据不是集中的会有多次datacenter的调用 在当前位置删除会导致最后只保留一个datacenter的网络端口组信息
    """
    if not netwrok_datas:  # 无更新数据
        return

    local_portgroups = {
        (item.name, item.host): item.id for item in db.network_port_group.list_all(platform_id)
    }

    dvs_local_portgroups = {
        (item.name, item.switch): item.id for item in db.network_dvs_port_group.dvs_portgroup_all(platform_id)
    }

    for networks, dc_name, dc_mor_name in netwrok_datas:
        for network in networks:
            if not isinstance(network, vim.dvs.DistributedVirtualPortgroup):  # Vswitch处理
                host_system = _get_portgroup_hostname(network.name, network.host)
                host_system_name = host_system.name if host_system else ''
                check_tuple = (network.name, host_system_name)
                if check_tuple in local_portgroups.keys():
                    local_portgroups.pop(check_tuple)
                
                network_mor_name = get_mor_name(network)
                sync_single_network_port_group(network.name, network_mor_name, dc_name, dc_mor_name, platform_id, host_system_name)
            else:  # Dvswitch处理
                dvswitch = _get_portgroup_dswitch(network)
                check_tuple = (network.name, dvswitch.name)
                if check_tuple in dvs_local_portgroups.keys():
                    dvs_local_portgroups.pop(check_tuple)
                
                network_mor_name = get_mor_name(network)
                sync_single_dvs_network_port_group(
                    network.name, network_mor_name, dc_name, dc_mor_name, platform_id, dvswitch.name, network.config.uplink)

    for item in local_portgroups:  # 清理vswitch部分的本地数据
        db.network_port_group.network_delete(local_portgroups[item])

    for item in dvs_local_portgroups:  # 清理dvswitch部分的本地数据
        db.network_dvs_port_group.dvs_network_delete(dvs_local_portgroups[item])


def sync_single_network_port_group(network_name, network_mor_name, dc_name, dc_mor_name, platform_id, host):
    """
    同步单个端口组信息  vswitch
    """
    # import pdb;pdb.set_trace()
    # pg_name = network.name if isinstance(network, vim.Network) else network.spec.name# network.name
    network_info = db.network_port_group.find_portgroup_by_name(network_name, host)  # change
    
    if not network_info:
        db.network_port_group.network_create(
            name=network_name, 
            mor_name=network_mor_name, 
            dc_name=dc_name, 
            dc_mor_name=dc_mor_name, 
            platform_id=platform_id, 
            host=host
        )
    else:
        db.network_port_group.network_update(
            id=network_info.id, 
            name=network_name, 
            mor_name=network_mor_name, 
            dc_name=dc_name,
            dc_mor_name=dc_mor_name
        )


def sync_single_dvs_network_port_group(network_name, network_mor_name, dc_name, dc_mor_name, platform_id, switch, uplink):
    """
    同步dswitch端口组信息
    """
    network_info = db.network_dvs_port_group.find_dvs_portgroup_by_name(network_name, switch)

    if not network_info:
        db.network_dvs_port_group.dvs_network_create(
            name=network_name,
            mor_name=network_mor_name,
            dc_name=dc_name,
            dc_mor_name=dc_mor_name,
            platform_id=platform_id,
            switch=switch,
            uplink=uplink
        )
    else:
        db.network_dvs_port_group.dvs_network_update(
            id=network_info.id,
            name=network_name,
            mor_name=network_mor_name,
            dc_name=dc_name,
            dc_mor_name=dc_mor_name
        )


def _get_portgroup_hostname(portgroup_name, network_host):
    """
    获取端口组的host信息
    """
    for item in network_host:
        for vss in item.config.network.portgroup:
            if vss.spec.name == portgroup_name:
                return item
    
    # raise Exception("Get portgroup's hostname Failed!!! {}, {}".format(portgroup_name, network_host))
    return None

def _get_portgroup_dswitch(network):
    """
    获取dvswitch
    """
    return network.config.distributedVirtualSwitch


def get_network_by_id(id):
    return db.network_port_group.network_list_by_id(id)

def get_dvs_network_by_id(id):
    return db.network_dvs_port_group.find_dvs_portgroup_by_id(id)

def get_network_port_group_all(platform_id):
    port_groups = db.network_port_group.list_all(platform_id)

    network_port_group_list = []

    for group in port_groups:
        group_tmp = dict()
        group_tmp['id'] = group.id
        group_tmp['name'] = group.name
        group_tmp['mor_name'] = group.mor_name
        group_tmp['dc_name'] = group.dc_name
        group_tmp['dc_mor_name'] = group.dc_mor_name
        group_tmp['platform_id'] = group.platform_id
        group_tmp['host'] = group.host

        network_port_group_list.append(group_tmp)
    return network_port_group_list


def get_dvs_network_port_group_all(platform_id):
    port_groups = db.network_dvs_port_group.dvs_portgroup_all(platform_id)

    network_port_group_list = []

    for group in port_groups:
        group_tmp = dict()
        group_tmp['id'] = group.id
        group_tmp['name'] = group.name
        group_tmp['mor_name'] = group.mor_name
        group_tmp['dc_name'] = group.dc_name
        group_tmp['dc_mor_name'] = group.dc_mor_name
        group_tmp['platform_id'] = group.platform_id
        group_tmp['switch'] = group.switch

        network_port_group_list.append(group_tmp)
    return network_port_group_list


def check_if_portgroup_exists(portgroup_id=None, portgroup_name=None, host_name=None):
    """
    检查端口组名称是否已经存在   Vswitch
    """
    if portgroup_id:
        return True if db.network_port_group.find_portgroup_by_id(portgroup_id) else False
    elif portgroup_name and host_name:
        return True if db.network_port_group.find_portgroup_by_name(portgroup_name, host_name) \
            else False
    else:
        raise Exception


def check_if_dvs_portgroup_exists(portgroup_id=None, portgroup_name=None, switch_name=None):
    """
    检查端口组名称是否已经存在  Dvswitch
    """
    if portgroup_id:
        return True if db.network_dvs_port_group.find_dvs_portgroup_by_id(portgroup_id) else False
    elif portgroup_name and switch_name:
        return True if db.network_dvs_port_group.find_dvs_portgroup_by_name(portgroup_name, switch_name) \
            else False
    else:
        raise Exception


class PortGroup:
    """
    vswitch的端口组管理
    """
    def __init__(self, platform_id):
        try:
            self._server_instance, self._content, self._platform = get_connect(platform_id)
        except Exception as e:
            raise Exception('Connect Vcenter Failed!')

        self._platform_id = platform_id

    def create_vswitch_portgroup(self, host_name, switch_name, portgroup_name):
        """
        创建vswitch端口组项
        """
        if not all([host_name, switch_name, portgroup_name]):
            raise Exception('Parameter Error!!!')
        
        _host_system = get_obj(self._content, [vim.HostSystem], host_name)
        _vdogm = VMPortGroupManager(_host_system)
        if not _vdogm.create_port_group(switch_name, portgroup_name):
            raise Exception("Create Vswitch PortGroup Failed!!!")
        
        # 同步本地  TODO
        dc = self._get_hostsystem_data_center(_host_system)
        sync_single_network_port_group(portgroup_name, '', dc.name, get_mor_name(dc), self._platform_id, host_name)

    def delete_vswitch_portgroup(self, host_name, portgroup_name):
        """
        删除vswitch端口组项
        """
        if not all([host_name, portgroup_name]):
            g.error_code = 5803
            raise Exception('Parameter Error!!!')

        _host_system = get_obj(self._content, [vim.HostSystem], host_name)
        _vdogm = VMPortGroupManager(_host_system)
        if not _vdogm.delete_port_group(portgroup_name):
            raise Exception("Destroy Vswitch PortGroup Failed!!!")
        
        # 同步本地  TODO
        network_info = db.network_port_group.find_portgroup_by_name(portgroup_name, host_name)  # change
        if network_info:
            db.network_port_group.network_delete(network_info.id)

    def delete_vswitch_portgroup_by_id(self, portgroup_id):
        item = db.network_port_group.find_portgroup_by_id(portgroup_id)
        self.delete_vswitch_portgroup(item.host, item.name)

    def _get_hostsystem_data_center(self, host_system):
        """
        通过host_system获取对应的data_center
        """
        host_system_networks = set(host_system.network)
        container = self._content.viewManager.CreateContainerView(
            self._content.rootFolder, [vim.Datacenter], True)
        for item in container.view:
            if not (host_system_networks - set(item.network)):
                return item
        
        return None


class DVSPortGroup:
    
    def __init__(self, platform_id):
        try:
            self._server_instance, self._content, self._platform = get_connect(platform_id)
        except Exception as e:
            raise Exception('Connect Vcenter Failed!')

        self._platform_id = platform_id

    def create_dvswitch_portgroup(self, switch_name, portgroup_name, port_num):
        """
        创建Dvswitch端口组项
        """
        if not all([switch_name, portgroup_name, port_num]):
            g.error_code = 5952
            raise Exception('Parameter Error!!!')
        
        _dv_switch = get_obj(self._content, [vim.DistributedVirtualSwitch], switch_name)
        _vdpgm = VMDvsPortGroupManager(_dv_switch)
        if not _vdpgm.create_port_group(portgroup_name, port_num):
            raise Exception('Create Dvswitch PortGroup Failed!!!')

        dc = self._get_dvswitch_data_center(_dv_switch)
        sync_single_dvs_network_port_group(portgroup_name, '', dc.name, get_mor_name(dc), self._platform_id, switch_name)

    def delete_dvswitch_portgroup(self, switch_name, portgroup_name):
        """
        删除Dvswitch端口组项
        """
        if not all([switch_name, portgroup_name]):
            g.error_code = 6002
            raise Exception('Parameter Error!!!')
        
        _dv_switch = get_obj(self._content, [vim.DistributedVirtualSwitch], switch_name)
        _vdpgm = VMDvsPortGroupManager(_dv_switch)
        if not _vdpgm.delete_port_group(portgroup_name):
            raise Exception('Create Dvswitch PortGroup Failed!!!')

        # 同步本地  TODO
        network_info = db.network_dvs_port_group.find_dvs_portgroup_by_name(portgroup_name, switch_name)
        if network_info:
            db.network_dvs_port_group.dvs_network_delete(network_info.id)

    def delete_dvswitch_portgroup_by_id(self, portgroup_id):
        item =  db.network_dvs_port_group.find_dvs_portgroup_by_id(portgroup_id)
        self.delete_dvswitch_portgroup(item.switch, item.name)

    def _get_dvswitch_data_center(self, dvswitch):
        """
        通过dvswitch获取对应的data_center
        """
        dvswitch_networks = set(dvswitch.portgroup)
        container = self._content.viewManager.CreateContainerView(
            self._content.rootFolder, [vim.Datacenter], True)
        for item in container.view:
            if not (dvswitch_networks - set(item.network)):
                return item
        
        return None
