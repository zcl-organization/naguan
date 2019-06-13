# -*- coding: utf-8 -*-
from pyVmomi import vim


class VMVswitchManager:
    def __init__(self, host_system):
        self._host_system = host_system

    def create(self, switch_name, number_of_ports, mtu, nics=None):
        vss_spec = vim.host.VirtualSwitch.Specification()
        vss_spec.numPorts = number_of_ports
        vss_spec.mtu = mtu
        if nics:
            vss_spec.bridge = vim.host.VirtualSwitch.BondBridge(nicDevice=nics)

        try:
            network_mgr = self._host_system.configManager.networkSystem
            if not network_mgr:
                raise RuntimeError
            
            network_mgr.AddVirtualSwitch(vswitchName=switch_name, spec=vss_spec)
        except Exception as e:
            return False
        
        return True

    def destroy(self, switch_name):
        try:
            self._host_system.configManager.networkSystem.RemoveVirtualSwitch(switch_name)
        except Exception as e:
            return False
        
        return True

    def update(self, switch_name, vswitch_old_infos, number_of_ports=None, mtu=None, nics=[]):
        diff = False    # 更改配置标记
        
        remain_pnic = []
        for desired_pnic in nics:
            if desired_pnic not in vswitch_old_infos['pnic']:
                remain_pnic.append(desired_pnic)

        all_nics = vswitch_old_infos['pnic']
        if remain_pnic:
            all_nics += remain_pnic
            diff = True
        if mtu and vswitch_old_infos['mtu'] != mtu:
            diff = True
        if number_of_ports and vswitch_old_infos['num_ports'] != number_of_ports:
            diff = True

        if not diff:
            return False

        # 避开默认参数值的干扰
        mtu = mtu if mtu else vswitch_old_infos['mtu']
        number_of_ports = number_of_ports if number_of_ports else vswitch_old_infos['num_ports']

        try:
            vss_spec = vim.host.VirtualSwitch.Specification()
            if all_nics:
                vss_spec.bridge = vim.host.VirtualSwitch.BondBridge(nicDevice=all_nics)
            vss_spec.numPorts = number_of_ports
            vss_spec.mtu = mtu

            network_mgr = self._host_system.configManager.networkSystem
            if not network_mgr:
                raise RuntimeError
            network_mgr.UpdateVirtualSwitch(vswitchName=switch_name, spec=vss_spec)
        except Exception as e:
            return False

        return True
