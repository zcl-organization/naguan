# -*- coding: utf-8 -*-
import json   # TODO 序列化方式变更不用json

from flask import g
from pyVmomi import vim

from app.main.vcenter import db
from app.main.vcenter.utils.base import VCenter
from app.main.vcenter.utils.vm_dvs import VMDvswitchManager
from app.main.vcenter.utils.vm_dvs import VMDvswitchHostManager
from app.main.vcenter.control.utils import get_mor_name


def sync_dvswitch(dvswitch_datas, platform_id):
    """
    同步数据
    """
    if not dvswitch_datas:
        return

    local_data = {(item.name, item.dc_name): item.id for item in db.dvswitch.dvswitch_all(platform_id)}

    for dvswitch in dvswitch_datas:

        data = dict(
            platform_id=platform_id,
            dc_name=dvswitch.parent.parent.name,
            dc_mor_name=get_mor_name(dvswitch.parent.parent),
            name=dvswitch.name,
            mor_name=get_mor_name(dvswitch),
            host_id='', 
            mtu=dvswitch.config.maxMtu,
            active_uplink_port=str(list(dvswitch.config.defaultPortConfig.uplinkTeamingPolicy.uplinkPortOrder.activeUplinkPort)),
            standby_uplink_port=str(list(dvswitch.config.defaultPortConfig.uplinkTeamingPolicy.uplinkPortOrder.standbyUplinkPort)),
            protocol=dvswitch.config.linkDiscoveryProtocolConfig.protocol,
            operation=dvswitch.config.linkDiscoveryProtocolConfig.operation,
            version=dvswitch.config.productInfo.version,
            describe=dvswitch.config.description,
            admin_name=dvswitch.config.contact.name,
            admin_describe=dvswitch.config.contact.contact,
            mulit_mode=dvswitch.config.multicastFilteringMode
        )
        
        if (dvswitch.name, dvswitch.parent.parent.name) in local_data.keys():
            data['dvswitch_id'] = local_data[(dvswitch.name, dvswitch.parent.parent.name)]
            db.dvswitch.dvswitch_update(**data)
            local_data.pop((dvswitch.name, dvswitch.parent.parent.name))
        else:
            db.dvswitch.dvswitch_create(**data)
    
    for item in local_data.values():
        db.dvswitch.dvswitch_delete(item)


def get_dvswitch_infos(platform_id, has_host):
    """
    获取本地所有的dvswitch信息
    """
    dvswitchs = db.dvswitch.dvswitch_all(platform_id)
    dvswitch_list = []

    for dvswitch in dvswitchs:
        if has_host and not dvswitch.host_id:
            continue

        dvs_item = dict(
            id=dvswitch.id,
            platform_id=dvswitch.platform_id,
            name=dvswitch.name,
            mor_name=dvswitch.mor_name,
            host_id=dvswitch.host_id,
            mtu=dvswitch.mtu,
            active_uplink_port=dvswitch.active_uplink_port,
            standby_uplink_port=dvswitch.standby_uplink_port,
            protocol=dvswitch.protocol,
            operation=dvswitch.operation,
            version=dvswitch.version,
            describe=dvswitch.describe,
            admin_name=dvswitch.admin_name,
            admin_describe=dvswitch.describe,
            mulit_mode=dvswitch.mulit_mode
        )

        dvswitch_list.append(dvs_item)

    return dvswitch_list


def check_if_dvswitch_exists(dvswitch_id=None, platform_id=None, name=None, dc_name=None):
    """
    检查vswitch是否存在
    """
    if dvswitch_id:
        return True if db.dvswitch.find_dvswitch_by_id(dvswitch_id) else False
    elif platform_id and name and dc_name:
        return True if db.dvswitch.find_dvswitch_by_name(platform_id, name, dc_name) else False
    else:
        raise RuntimeError("Check Failed!!!")


class DVSwitch:

    def __init__(self, platform_id):
        self._platform_id = platform_id
        self._vcenter = VCenter(platform_id)

    def create_dvswitch(self, args):
        """
        创建vswitch
        """
        if check_if_dvswitch_exists(
                platform_id=args['platform_id'], name=args['switch_name'], 
                dc_name=args['dc_name']):
            g.error_code = 6553
            raise RuntimeError("Project Already Exists!!!")

        build_data = dict(
            switch_name=args['switch_name'],
            mtu=int(args['mtu']) if args['mtu'] else 1500,
            discovery_protocol=args['protocol'] if args['protocol'] else 'cdp',
            discovery_operation=args['operation'] if args['operation'] else 'listen',
            uplink_quantity=int(args['uplink_quantity']) if args['uplink_quantity'] else 4,
            uplink_prefix=args['uplink_prefix'] if args['uplink_prefix'] else 'dvs ',
            switch_version=args['switch_version'] if args['switch_version'] else '6.6.0'
        )

        # balabala...
        datacenter = self._vcenter.find_datacenter_by_name(args['dc_name'])
        folder = self._find_folder_by_name(datacenter)  # TODO 待更新现在的操作是直接返回数据中心下的根目录项

        vmdvsm = VMDvswitchManager(self._vcenter.connect, folder)
        if not vmdvsm.create(**build_data):
            raise RuntimeError("Create VSwitch Failed!!!")
        
        # 同步
        dvs = self._find_dvs_by_name(args['switch_name'], folder)
        data = dict(
            platform_id=args['platform_id'],
            dc_name=dvs.parent.parent.name,
            dc_mor_name=get_mor_name(dvs.parent.parent),
            name=dvs.name,
            mor_name=get_mor_name(dvs),
            host_id='', 
            mtu=dvs.config.maxMtu,
            active_uplink_port=str(list(dvs.config.defaultPortConfig.uplinkTeamingPolicy.uplinkPortOrder.activeUplinkPort)),
            standby_uplink_port=str(list(dvs.config.defaultPortConfig.uplinkTeamingPolicy.uplinkPortOrder.standbyUplinkPort)),
            protocol=dvs.config.linkDiscoveryProtocolConfig.protocol,
            operation=dvs.config.linkDiscoveryProtocolConfig.operation,
            version=dvs.config.productInfo.version,
            describe=dvs.config.description,
            admin_name=dvs.config.contact.name,
            admin_describe=dvs.config.contact.contact,
            mulit_mode=dvs.config.multicastFilteringMode
        )
        db.dvswitch.dvswitch_create(**data)
    
    def delete_dvswitch_by_name(self, switch_name, dc_name):
        """
        通过名称删除dvswitch
        """
        datacenter = self._vcenter.find_datacenter_by_name(dc_name)
        vmdvsm = VMDvswitchManager(self._vcenter.connect, datacenter=datacenter)
        if not vmdvsm.destroy(switch_name):
            raise RuntimeError("Destroy VSwitch Failed!!!")

    def delete_dvswitch_by_id(self, dvswitch_id):
        """
        通过标识id删除dvswitch
        """
        data = db.dvswitch.find_dvswitch_by_id(dvswitch_id)
        if not data:
            g.error_code = 6603
            raise RuntimeError("Project Does Not Exists!!!")

        self.delete_dvswitch_by_name(data.name, data.dc_name)

        db.dvswitch.dvswitch_delete(dvswitch_id)

    def update_dvswich(self, dvswitch_id, args):
        """
        更新dvswitch
        """
        data = db.dvswitch.find_dvswitch_by_id(dvswitch_id)
        if not data:
            g.error_code = 6653
            raise RuntimeError('Project Does Not Exists!!!')

        old_data = dict(
            mtu=data.mtu,
            link_protocol={
                "protocol": data.protocol,
                "operation": data.operation
            },
            uplink_name=data.active_uplink_port+data.standby_uplink_port, 
            switch_version=data.version
        )

        vmdvsm = VMDvswitchManager(self._vcenter.connect)
        # update mtu
        if args['mtu'] and old_data['mtu'] != args['mtu']:
            if not vmdvsm.update_mtu(data.name, int(args['mtu'])):
                raise RuntimeError("Update DVSwitch MTU Failed!!!")
        
        # update link protocol
        if args['protocol'] and args['operation'] and\
            old_data['link_protocol']['protocol'] != args['protocol'] and\
                old_data['link_protocol']['operation'] != args['operation']:
            if not vmdvsm.update_link_protocol(data.name, args['protocol'], args['operation']):
                raise RuntimeError("Updata DVSwitch Uplink Protocol Failed!!!")
        
        # update uplink name
        if (args['old_uplink_name'] or args['new_uplink_name']) and args['old_uplink_name'] in old_data['uplink_name']:
            if not vmdvsm.update_uplink_name(
                    data.name, args['uplink_operation'], args['old_uplink_name'], args['new_uplink_name']):
                raise RuntimeError('Updata DVSwitch UplinkName Failed!!!')
        
        # update switch name
        if args['switch_version'] and args['switch_version'] != old_data['switch_version']:
            if not vmdvsm.update_switch_version(data.name, args['switch_version']):
                raise RuntimeError("Update DVSwitch Version Failed!!!")
        
        # TODO 同步
        datacenter = self._vcenter.find_datacenter_by_name(data.dc_name)
        folder = self._find_folder_by_name(datacenter)
        dvs = self._find_dvs_by_name(data.name, folder)
        data = dict(
            dvswitch_id=dvswitch_id,
            platform_id=args['platform_id'],
            dc_name=dvs.parent.parent.name,
            dc_mor_name=get_mor_name(dvs.parent.parent),
            name=dvs.name,
            mor_name=get_mor_name(dvs),
            host_id='', 
            mtu=dvs.config.maxMtu,
            active_uplink_port=str(list(dvs.config.defaultPortConfig.uplinkTeamingPolicy.uplinkPortOrder.activeUplinkPort)),
            standby_uplink_port=str(list(dvs.config.defaultPortConfig.uplinkTeamingPolicy.uplinkPortOrder.standbyUplinkPort)),
            protocol=dvs.config.linkDiscoveryProtocolConfig.protocol,
            operation=dvs.config.linkDiscoveryProtocolConfig.operation,
            version=dvs.config.productInfo.version,
            describe=dvs.config.description,
            admin_name=dvs.config.contact.name,
            admin_describe=dvs.config.contact.contact,
            mulit_mode=dvs.config.multicastFilteringMode
        )
        db.dvswitch.dvswitch_update(**data)

    def _find_dvs_by_name(self, dvswitch_name, folder=None):
        content = self._vcenter.connect
        if not folder:
            folder = content.rootFolder
        
        container = content.viewManager.CreateContainerView(folder, [vim.DistributedVirtualSwitch], True)
        
        for dvswitch in container.view:
            if dvswitch.name == dvswitch_name:
                return dvswitch

        return None

    def _find_folder_by_name(self, datacenter):
        return datacenter.networkFolder


class DVSwitchHost:

    def __init__(self, platform_id):
        self._vcenter = VCenter(platform_id)

    def add_host(self, dvswitch_id, args):
        datacenter = self._vcenter.find_datacenter_by_name(args['dc_name'])
        if not datacenter:
            g.error_code = 6703
            raise RuntimeError("No corresponding datacenter")
        
        folder = datacenter.networkFolder
        data = db.dvswitch.find_dvswitch_by_id(dvswitch_id)
        if not data:
            g.error_code = 6704
            raise RuntimeError("Local no corresponding DVSwitch")
        
        dvs = self._get_object([vim.DistributedVirtualSwitch], data.name, folder)
        if not dvs:
            g.error_code = 6705
            raise RuntimeError("Remote no corresponding DVSwitch")

        host = self._vcenter.find_hostsystem_by_name(args['host_name'])
        if not host:
            g.error_code = 6706
            raise RuntimeError("No corresponding HostSystem")

        vmdhm = VMDvswitchHostManager(dvs)
        vmnics = args['vmnics'] if args['vmnics'] else []
        if not vmdhm.add(host, vmnics):
            raise RuntimeError("add Host {} To Switch {} Failed!!!".format(
                args['host_name'], args['switch_name']))

    def remove_host(self, dvswitch_id, args):
        datacenter = self._vcenter.find_datacenter_by_name(args['dc_name'])
        if not datacenter:
            g.error_code = 6733
            raise RuntimeError("No corresponding datacenter")

        folder = datacenter.networkFolder
        data = db.dvswitch.find_dvswitch_by_id(dvswitch_id)
        if not data:
            g.error_code = 6734
            raise RuntimeError("Local no corresponding DVSwitch")

        dvs = self._get_object([vim.DistributedVirtualSwitch], data.name, folder)
        if not dvs:
            g.error_code = 6735
            raise RuntimeError("Remote no corresponding DVSwitch")

        host = self._vcenter.find_hostsystem_by_name(args['host_name'])
        if not dvs or not host:
            g.error_code = 6736
            raise RuntimeError("No corresponding HostSystem")
        vmdhm = VMDvswitchHostManager(dvs)
        if not vmdhm.remove(host):
            raise RuntimeError("Remove Host {} To Switch {} Failed!!!".format(
                args['host_name'], args['switch_name']))

    def edit_host(self, dvswitch_id, args):
        datacenter = self._vcenter.find_datacenter_by_name(args['dc_name'])
        if not datacenter:
            g.error_code = 6763
            raise RuntimeError("No corresponding datacenter")

        folder = datacenter.networkFolder
        data = db.dvswitch.find_dvswitch_by_id(dvswitch_id)
        if not data:
            g.error_code = 6764
            raise RuntimeError("Local no corresponding DVSwitch")

        dvs = self._get_object([vim.DistributedVirtualSwitch], data.name, folder)
        if not dvs:
            g.error_code = 6765
            raise RuntimeError("Remote no corresponding DVSwitch")

        host = self._vcenter.find_hostsystem_by_name(args['host_name'])
        if not host:
            g.error_code = 6766
            raise RuntimeError("No corresponding HostSystem")

        vmdhm = VMDvswitchHostManager(dvs)
        vmnics = args['vmnics'] if args['vmnics'] else []
        if not vmdhm.edit(host, vmnics):
            raise RuntimeError("Edit Host {} To Switch {} Failed!!!".format(
                args['host_name'], args['switch_name']))

    def _get_object(self, vim_type, name, folder):
        if not folder:
            folder = self._vcenter.connect.rootFolder
            
        container = self._vcenter._connect.viewManager.CreateContainerView(folder, vim_type, True)
        for managed_object_ref in container.view:
            if managed_object_ref.name == name:
                return managed_object_ref

        return None