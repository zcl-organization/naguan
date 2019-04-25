# -*- coding:utf-8 -*-

from app.main.vcenter.control import get_mor_name, wait_for_tasks, get_obj
from app.main.vcenter.db import instances as db_vm
from app.main.vcenter.control.vcenter import get_connect
from app.main.vcenter.control import network_port_group as network_port_group_manage
from app.main.vcenter.control import network_devices as network_device_manage
from app.main.vcenter.db import vcenter as db_vcenter
from flask_restful.representations import json
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import atexit

import json


class Instance(object):

    def __init__(self, platform_id, uuid=None, si=None, content=None, network_port_group=None,
                 network_device=None):
        print('platform_id:', platform_id)
        self.platform_id = platform_id
        self.si = si
        self.content = content
        self.uuid = uuid

        if not si:
            try:
                si, content, platform = get_connect(platform_id)
                self.si = si
                self.content = content
                self.platform = platform
            except Exception as e:
                raise Exception('connect vcenter failed')
        else:
            self.platform = None
        if network_port_group:
            self.network_port_group = json.loads(network_port_group)
        else:
            self.network_port_group = None
        if network_device:
            self.network_device = json.loads(network_device)
        else:
            self.network_device = None

        if uuid:
            local_vm = db_vm.list_by_uuid(self.platform_id, self.uuid)
            vm = get_obj(self.content, [vim.VirtualMachine], local_vm.vm_name)

            self.local_vm = local_vm
            self.vm = vm
        else:
            self.local_vm = None
            self.vm = None

    # 开机
    def start(self):
        try:

            task = self.vm.PowerOn()
            wait_for_tasks(self.si, [task])
        except Exception as e:
            raise Exception('vm start failed')

    # 关机
    def stop(self, force=True):
        try:
            if not force:
                task = self.vm.ShutdownGuest()
                wait_for_tasks(self.si, [task])
            else:
                task = self.vm.PowerOff()
                wait_for_tasks(self.si, [task])
        except Exception as e:
            raise Exception('vm stop failed')

    # 暂停
    def suspend(self, force=True):
        try:

            if not force:
                task = self.vm.StandbyGuest()
                wait_for_tasks(self.si, [task])
            else:
                task = self.vm.Suspend()
                wait_for_tasks(self.si, [task])
        except Exception as e:
            raise Exception('vm suspend failed')

    # 重启
    def restart(self):
        task = self.vm.ResetVM_Task()
        wait_for_tasks(self.si, [task])

    def delete(self):
        task = self.vm.Destroy()
        wait_for_tasks(self.si, [task])

    def add_network(self, networks):
        networks = json.loads(networks)

        devs = self.vm.config.hardware.device

        # nic_prefix_label = 'Network adapter '

        for network in networks:

            # 获取网络设备信息
            local_network_port_group = network_port_group_manage.get_network_by_id(network)

            # 开始添加网卡信息
            spec = vim.vm.ConfigSpec()
            nic_changes = []

            nic_spec = vim.vm.device.VirtualDeviceSpec()
            nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            nic_spec.device = vim.vm.device.VirtualE1000()
            nic_spec.device.deviceInfo = vim.Description()
            nic_spec.device.deviceInfo.summary = 'vCenter API test'

            # content = self.si.RetrieveContent()

            network = get_obj(self.content, [vim.Network], local_network_port_group.name)
            if isinstance(network, vim.OpaqueNetwork):

                nic_spec.device.backing = \
                    vim.vm.device.VirtualEthernetCard.OpaqueNetworkBackingInfo()
                nic_spec.device.backing.opaqueNetworkType = \
                    network.summary.opaqueNetworkType
                nic_spec.device.backing.opaqueNetworkId = \
                    network.summary.opaqueNetworkId
            else:

                nic_spec.device.backing = \
                    vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
                nic_spec.device.backing.useAutoDetect = False
                nic_spec.device.backing.deviceName = network.name

            nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
            nic_spec.device.connectable.startConnected = True
            nic_spec.device.connectable.allowGuestControl = True
            nic_spec.device.connectable.connected = False
            nic_spec.device.connectable.status = 'untried'
            nic_spec.device.wakeOnLanEnabled = True
            nic_spec.device.addressType = 'assigned'

            nic_changes.append(nic_spec)
            spec.deviceChange = nic_changes
            task = self.vm.ReconfigVM_Task(spec=spec)
            wait_for_tasks(self.si, [task])

    def del_network(self, networks):
        try:
            networks = json.loads(networks)

            devs = self.vm.config.hardware.device

            # 获取network device label
            for device_id in networks:

                # 根据id 获取 network device
                device = network_device_manage.device_list_by_id(self.platform_id, self.uuid, device_id)

                if device:
                    for dev in devs:
                        virtual_nic_device = None
                        if isinstance(dev, vim.vm.device.VirtualEthernetCard) \
                                and device.label == dev.deviceInfo.label:
                            virtual_nic_device = dev

                        if virtual_nic_device:
                            virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
                            virtual_nic_spec.operation = \
                                vim.vm.device.VirtualDeviceSpec.Operation.remove
                            virtual_nic_spec.device = virtual_nic_device

                            spec = vim.vm.ConfigSpec()
                            spec.deviceChange = [virtual_nic_spec]
                            task = self.vm.ReconfigVM_Task(spec=spec)
                            wait_for_tasks(self.si, [task])

                else:
                    raise Exception('unable find vm network device')
        except Exception as e:
            Exception('vm network delete failed')

    def update_vcpu(self, new_cpu, old_cpu):
        try:
            if self.local_vm.cpu == old_cpu:
                cspec = vim.vm.ConfigSpec()
                cspec.numCPUs = int(new_cpu)
                cspec.numCoresPerSocket = 1
                task = self.vm.Reconfigure(cspec)
                wait_for_tasks(self.si, [task])
            else:
                raise Exception('参数错误')
        except Exception as e:
            raise Exception('vm cpu update failed')

    def update_vmemory(self, new_memory, old_memory):
        try:
            if self.local_vm.memory == old_memory:
                print ('cccc')
                cspec = vim.vm.ConfigSpec()
                cspec.memoryMB = int(new_memory)
                task = self.vm.Reconfigure(cspec)
                wait_for_tasks(self.si, [task])
            else:
                raise Exception('参数错误')
        except Exception as e:
            raise Exception('vm memory update failed')

    def boot(self, new_cpu, new_memory, dc_id, ds_id, vm_name, networks):
        try:
            dc_info = db_vcenter.vcenter_tree_by_id(dc_id)
            dc = get_obj(self.content, [vim.Datacenter], dc_info.name)

            # print(dc)
            vm_folder = dc.vmFolder
            hosts = dc.hostFolder.childEntity
            resource_pool = hosts[0].resourcePool

            # ds = content.viewManager.CreateContainerView(dc, [vim.Datastore], True)

            ds = get_obj(self.content, [vim.Datastore], 'datastore1')

            # datastore_path = '[' + ds + '] ' + vm_name
            datastore_path = '[datastore1]' + vm_name

            vmx_file = vim.vm.FileInfo(logDirectory=None,
                                       snapshotDirectory=None,
                                       suspendDirectory=None,
                                       vmPathName=datastore_path)

            config = vim.vm.ConfigSpec(
                name=vm_name,
                memoryMB=int(new_memory),
                numCPUs=int(new_cpu),
                files=vmx_file,
                guestId='rhel6_64Guest',
                version='vmx-09'
            )

            task = vm_folder.CreateVM_Task(config=config, pool=resource_pool)
            wait_for_tasks(self.si, [task])

            # 获取vm 并为vm 添加network
            vm = get_obj(self.content, [vim.VirtualMachine], vm_name)
            self.add_network(networks)
            # vm_add_network(self.platform_id, vm.summary.config.uuid, networks, vm)
        except Exception as e:
            raise Exception('vm create failed')

    def list(self, host, vm_name):
        try:
            vms = db_vm.vm_list(self.platform_id, host, vm_name)
            vm_list = []
            if vms:
                for vm in vms:
                    vm_temp = dict()
                    vm_temp['id'] = vm.id
                    vm_temp['platform_id'] = vm.platform_id
                    vm_temp['vm_name'] = vm.vm_name
                    vm_temp['vm_mor_name'] = vm.vm_mor_name
                    vm_temp['template'] = vm.template
                    vm_temp['vm_path_name'] = vm.vm_path_name
                    vm_temp['memory'] = vm.memory
                    vm_temp['cpu'] = vm.cpu
                    vm_temp['num_ethernet_cards'] = vm.num_ethernet_cards
                    vm_temp['num_virtual_disks'] = vm.num_virtual_disks
                    vm_temp['uuid'] = vm.uuid
                    vm_temp['instance_uuid'] = vm.instance_uuid
                    vm_temp['guest_id'] = vm.guest_id
                    vm_temp['guest_full_name'] = vm.guest_full_name
                    vm_temp['host'] = vm.host
                    vm_temp['guest_id'] = vm.guest_id
                    vm_temp['ip'] = vm.ip
                    vm_temp['status'] = vm.status
                    vm_list.append(vm_temp)
        except Exception as e:
            raise Exception('vm list get failed')
        return vm_list

    def list_by_uuid(self, uuid):
        vm = db_vm.list_by_uuid(self.platform_id, uuid)
        vm_temp = dict()
        vm_temp['id'] = vm.id
        vm_temp['platform_id'] = vm.platform_id
        vm_temp['vm_name'] = vm.vm_name
        vm_temp['vm_mor_name'] = vm.vm_mor_name
        vm_temp['template'] = vm.template
        vm_temp['vm_path_name'] = vm.vm_path_name
        vm_temp['memory'] = vm.memory
        vm_temp['cpu'] = vm.cpu
        vm_temp['num_ethernet_cards'] = vm.num_ethernet_cards
        vm_temp['num_virtual_disks'] = vm.num_virtual_disks
        vm_temp['uuid'] = vm.uuid
        vm_temp['instance_uuid'] = vm.instance_uuid
        vm_temp['guest_id'] = vm.guest_id
        vm_temp['guest_full_name'] = vm.guest_full_name
        vm_temp['host'] = vm.host
        vm_temp['guest_id'] = vm.guest_id
        vm_temp['ip'] = vm.ip
        vm_temp['status'] = vm.status
        return vm_temp

    def sync_db(self):
        pass

#
# def vm_list_all(platform_id, host, vm_name):
#     vms = db_vm.vm_list(platform_id, host, vm_name)
#     vm_list = []
#     if vms:
#         for vm in vms:
#             vm_temp = dict()
#             vm_temp['id'] = vm.id
#             vm_temp['platform_id'] = vm.platform_id
#             vm_temp['vm_name'] = vm.vm_name
#             vm_temp['vm_mor_name'] = vm.vm_mor_name
#             vm_temp['template'] = vm.template
#             vm_temp['vm_path_name'] = vm.vm_path_name
#             vm_temp['memory'] = vm.memory
#             vm_temp['cpu'] = vm.cpu
#             vm_temp['num_ethernet_cards'] = vm.num_ethernet_cards
#             vm_temp['num_virtual_disks'] = vm.num_virtual_disks
#             vm_temp['uuid'] = vm.uuid
#             vm_temp['instance_uuid'] = vm.instance_uuid
#             vm_temp['guest_id'] = vm.guest_id
#             vm_temp['guest_full_name'] = vm.guest_full_name
#             vm_temp['host'] = vm.host
#             vm_temp['guest_id'] = vm.guest_id
#             vm_temp['ip'] = vm.ip
#             vm_temp['status'] = vm.status
#             vm_list.append(vm_temp)
#     return vm_list

#
# def power_action(action, platform_id, uuid):
#     s, content, platform = get_connect(platform_id)
#
#     vm = db_vm.list_by_uuid(platform['id'], uuid)
#     vm_name = vm.vm_name
#     vm = get_obj(content, [vim.VirtualMachine], vm_name)
#
#     # print(vm)
#     force = True
#     if action == 'start':
#         # invoke_and_track(vm.PowerOn, None)
#         task = vm.PowerOn()
#         wait_for_tasks(s, [task])
#
#     elif action == 'stop':
#         if not force:
#             task = vm.ShutdownGuest()
#             wait_for_tasks(s, [task])
#             # invoke_and_track(vm.ShutdownGuest)
#             # wait_for_tasks(s, vm.ShutdownGuest)
#         else:
#             task = vm.PowerOff()
#             wait_for_tasks(s, [task])
#             # invoke_and_track(vm.PowerOff)
#
#     elif action == 'suspend':
#         if not force:
#             task = vm.StandbyGuest()
#             wait_for_tasks(s, [task])
#         else:
#             task = vm.Suspend()
#             wait_for_tasks(s, [task])
#     elif action == 'restart':
#         task = vm.ResetVM_Task()
#         wait_for_tasks(s, [task])

#
# def vm_delete(platform_id, uuid):
#     s, content, platform = get_connect(platform_id)
#
#     local_vm = db_vm.list_by_uuid(platform['id'], uuid)
#     vm_name = local_vm.vm_name
#     vm = get_obj(content, [vim.VirtualMachine], vm_name)
#
#     task = vm.Destroy()
#     wait_for_tasks(s, [task])

#
# def vm_update_cpu(platform_id, uuid, new_cpu, old_cpu):
#     s, content, platform = get_connect(platform_id)
#
#     local_vm = db_vm.list_by_uuid(platform['id'], uuid)
#
#     if local_vm.cpu == old_cpu:
#         vm_name = local_vm.vm_name
#         vm = get_obj(content, [vim.VirtualMachine], vm_name)
#
#         cspec = vim.vm.ConfigSpec()
#         cspec.numCPUs = int(new_cpu)
#         cspec.numCoresPerSocket = 1
#         task = vm.Reconfigure(cspec)
#         wait_for_tasks(s, [task])
#         print('update success cpu')
#     else:
#         raise Exception('参数错误')

#
# def vm_update_memory(platform_id, uuid, new_memory, old_memory):
#     s, content, platform = get_connect(platform_id)
#
#     local_vm = db_vm.list_by_uuid(platform['id'], uuid)
#
#     if local_vm.memory == old_memory:
#         vm_name = local_vm.vm_name
#         vm = get_obj(content, [vim.VirtualMachine], vm_name)
#
#         cspec = vim.vm.ConfigSpec()
#         cspec.memoryMB = int(new_memory)
#         task = vm.Reconfigure(cspec)
#         wait_for_tasks(s, [task])
#         print('update success memory')
#     else:
#         raise Exception('参数错误')

#
# def vm_add_network(platform_id, uuid, networks, vm=None):
#     # print(networks)
#     # networkS = json.load(networks)
#     networks = json.loads(networks)
#     # print(networkS)
#
#     print(1)
#     s, content, platform = get_connect(platform_id)
#     if not vm:
#         local_vm = db_vm.list_by_uuid(platform['id'], uuid)
#
#         vm = get_obj(content, [vim.VirtualMachine], local_vm.vm_name)
#
#     devs = vm.config.hardware.device
#     # print(devs)
#     nic_prefix_label = 'Network adapter '
#     print(2)
#     for network in networks:
#
#         # 获取网络设备信息
#         local_network_port_group = network_port_group_manage.get_network_by_id(network)
#
#         # 开始添加网卡信息
#         spec = vim.vm.ConfigSpec()
#         nic_changes = []
#
#         nic_spec = vim.vm.device.VirtualDeviceSpec()
#         nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
#
#         nic_spec.device = vim.vm.device.VirtualE1000()
#
#         nic_spec.device.deviceInfo = vim.Description()
#         nic_spec.device.deviceInfo.summary = 'vCenter API test'
#
#         content = s.RetrieveContent()
#
#         network = get_obj(content, [vim.Network], local_network_port_group.name)
#         if isinstance(network, vim.OpaqueNetwork):
#
#             nic_spec.device.backing = \
#                 vim.vm.device.VirtualEthernetCard.OpaqueNetworkBackingInfo()
#             nic_spec.device.backing.opaqueNetworkType = \
#                 network.summary.opaqueNetworkType
#             nic_spec.device.backing.opaqueNetworkId = \
#                 network.summary.opaqueNetworkId
#         else:
#
#             nic_spec.device.backing = \
#                 vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
#             nic_spec.device.backing.useAutoDetect = False
#             nic_spec.device.backing.deviceName = network.name
#
#         nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
#         nic_spec.device.connectable.startConnected = True
#         nic_spec.device.connectable.allowGuestControl = True
#         nic_spec.device.connectable.connected = False
#         nic_spec.device.connectable.status = 'untried'
#         nic_spec.device.wakeOnLanEnabled = True
#         nic_spec.device.addressType = 'assigned'
#
#         nic_changes.append(nic_spec)
#         spec.deviceChange = nic_changes
#         task = vm.ReconfigVM_Task(spec=spec)
#         wait_for_tasks(s, [task])

#
# def vm_del_network(platform_id, uuid, networks):
#     networks = json.loads(networks)
#
#     s, content, platform = get_connect(platform_id)
#     local_vm = db_vm.list_by_uuid(platform['id'], uuid)
#
#     vm = get_obj(content, [vim.VirtualMachine], local_vm.vm_name)
#
#     devs = vm.config.hardware.device
#     # 获取network device label
#
#     for device_id in networks:
#         # 根据id 获取 network device
#         device = network_device_manage.device_list_by_id(platform_id, uuid, device_id)
#         # print(device.label)
#         if device:
#             for dev in devs:
#                 # print(dev)
#                 virtual_nic_device = None
#                 # db_network.network_device_info_create(platform_id, )
#                 if isinstance(dev, vim.vm.device.VirtualEthernetCard) \
#                         and device.label == dev.deviceInfo.label:
#                     print(dev.deviceInfo.label)
#                     virtual_nic_device = dev
#
#                 if virtual_nic_device:
#                     # raise RuntimeError('Virtual {} could not be found.'.format(device.label))
#                     # print(dev.deviceInfo.label)
#
#                     virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
#                     virtual_nic_spec.operation = \
#                         vim.vm.device.VirtualDeviceSpec.Operation.remove
#                     virtual_nic_spec.device = virtual_nic_device
#
#                     spec = vim.vm.ConfigSpec()
#                     spec.deviceChange = [virtual_nic_spec]
#                     task = vm.ReconfigVM_Task(spec=spec)
#                     wait_for_tasks(s, [task])
#
#         else:
#             print('unable to find device')

#
# def create_vm(platform_id, new_cpu, new_memory, dc_id, ds_id, vm_name, networks):
#     s, content, platform = get_connect(platform_id)
#
#     dc_info = db_vcenter.vcenter_tree_by_id(dc_id)
#     dc = get_obj(content, [vim.Datacenter], dc_info.name)
#
#     # print(dc)
#     vm_folder = dc.vmFolder
#     hosts = dc.hostFolder.childEntity
#     resource_pool = hosts[0].resourcePool
#
#     # ds = content.viewManager.CreateContainerView(dc, [vim.Datastore], True)
#
#     ds = get_obj(content, [vim.Datastore], 'datastore1')
#     # print(ds)
#     # datastore_path = '[' + ds + '] ' + vm_name
#     datastore_path = '[datastore1]' + vm_name
#
#     vmx_file = vim.vm.FileInfo(logDirectory=None,
#                                snapshotDirectory=None,
#                                suspendDirectory=None,
#                                vmPathName=datastore_path)
#
#     config = vim.vm.ConfigSpec(
#         name=vm_name,
#         memoryMB=int(new_memory),
#         numCPUs=int(new_cpu),
#         files=vmx_file,
#         guestId='rhel6_64Guest',
#         version='vmx-09'
#     )
#     # print(vmx_file)
#     task = vm_folder.CreateVM_Task(config=config, pool=resource_pool)
#     wait_for_tasks(s, [task])
#     vm = get_obj(content, [vim.VirtualMachine], vm_name)
#     # print('uuid:', vm.summary.config.uuid)
#     vm_add_network(platform_id, vm.summary.config.uuid, networks, vm)
