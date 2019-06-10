# -*- coding:utf-8 -*-
from pyVmomi import vim
from pyVim.task import WaitForTask


class VMPortGroupManager:

    def __init__(self, host_system):
        self._host_system = host_system

    def create_port_group(self, vswitch_name, portgroup_name, vlan_id=0):
        """
        创建端口组
        """
        port_group = vim.host.PortGroup.Config()
        port_group.spec = vim.host.PortGroup.Specification()
        port_group.spec.vswitchName = vswitch_name
        port_group.spec.name = portgroup_name
        port_group.spec.vlanId = vlan_id
        # TODO 配置项的优化   目前提供的能力是最为基础的配置项
        port_group.spec.policy = vim.host.NetworkPolicy()

        try:
            self._host_system.configManager.networkSystem.AddPortGroup(
                portgrp=port_group.spec)
        except Exception as e:
            return False
        
        return True

    def delete_port_group(self, portgroup_name):
        """
        删除端口组
        """
        try:
            self._host_system.configManager.networkSystem.RemovePortGroup(
                pgName=portgroup_name)
        except Exception as e:
            return False
        
        return True
    

class VMDvsPortGroupManager:
    
    def __init__(self, dv_switch):
        self._dv_switch = dv_switch

    def create_port_group(self, portgroup_name, num_ports, portgroup_type='earlyBinding', vlan_id=0):
        """
        创建端口组
        TODO 目前已知的portgroup_type类型只有earlyBinding  需要查询出更多类型  2019.06.04
        """
        config = vim.dvs.DistributedVirtualPortgroup.ConfigSpec()

        config.name = portgroup_name
        config.numPorts = num_ports
        # TODO 配置项的优化   目前提供的能力是最为基础的配置项
        config.defaultPortConfig = vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy()
        config.defaultPortConfig.vlan = vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec()
        config.defaultPortConfig.vlan.vlanId = vlan_id
        config.defaultPortConfig.vlan.inherited = False
        config.defaultPortConfig.securityPolicy = vim.dvs.VmwareDistributedVirtualSwitch.SecurityPolicy()
        teamingPolicy = vim.dvs.VmwareDistributedVirtualSwitch.UplinkPortTeamingPolicy()
        config.defaultPortConfig.uplinkTeamingPolicy = teamingPolicy
        config.policy = vim.dvs.VmwareDistributedVirtualSwitch.VMwarePortgroupPolicy()
        config.type = portgroup_type

        try:
            task = self._dv_switch.AddDVPortgroup_Task([config])
            WaitForTask(task)
        except Exception as e:
            return False

        return True

    def delete_port_group(self, portgroup_name):
        """
        删除端口组
        """
        dvs_portgroup = self._find_portgroup_by_name(portgroup_name)

        try:
            task = dvs_portgroup.Destroy_Task()
            WaitForTask(task)
        except Exception as e:
            return False

        return True

    def _find_portgroup_by_name(self, portgroup_name):
        for pg in self._dv_switch.portgroup:
            if pg.name == portgroup_name:
                return pg

        raise Exception('No Find DVS PortGroup')
