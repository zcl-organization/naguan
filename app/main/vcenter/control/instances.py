# -*- coding:utf-8 -*-
from flask import g

from app.main.vcenter.control.utils import get_mor_name, wait_for_tasks, get_obj, get_connect, validate_input
from app.main.vcenter.control.disks import sync_disk
from app.main.vcenter.control.network_devices import sync_network_device

from app.main.vcenter.control import network_port_group as network_port_group_manage
from app.main.vcenter.control import network_devices as network_device_manage
from app.main.vcenter.control import snapshots as snapshot_nanage
from app.main.vcenter.control import disks as disk_manage
from flask_restful.representations import json
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
from pyVim.task import WaitForTask, WaitForTasks
import atexit

import json

from app.main.vcenter import db
from app.main.vcenter.utils.vm_manager import VMMaintainBaseManager
from app.main.vcenter.utils.vm_manager import VMMaintainSnapshotManager
from app.main.vcenter.utils.vm_manager import VMDeviceInfoManager


class Instance(object):

    def __init__(self, platform_id, uuid=None, si=None, content=None, network_port_group=None, network_device=None):
        self.platform_id = platform_id
        self.si = si
        self.content = content
        self.uuid = uuid

        if not si:
            try:
                self.si, self.content, self.platform = get_connect(platform_id)
            except Exception as e:
                raise Exception('connect vcenter failed')
        else:
            self.platform = None

        # TODO
        self.network_port_group = json.loads(network_port_group) if network_port_group else None
        self.network_device = json.loads(network_device) if network_device else None

        self._vm_device_info_manager = VMDeviceInfoManager(self.si, self.content)
        if uuid:
            self.local_vm = db.instances.list_by_uuid(self.platform_id, self.uuid)
            vm = get_obj(self.content, [vim.VirtualMachine], self.local_vm.vm_name)
            self._set_vm(vm)
        else:
            self.local_vm = None
            self._set_vm(None)

    def _set_vm(self, vm):
        if vm:
            self.vm = vm
            self._vm_base_manager = VMMaintainBaseManager(vm)
            self._vm_snapshot_manager = VMMaintainSnapshotManager(vm)
            self._vm_device_info_manager.vm = vm
        else:
            self._vm = None
            self._vm_base_manager = None
            self._vm_snapshot_manager = None
            self._vm_device_info_manager.vm = None

    def start(self):
        """
        虚拟机实例开机
        """
        if self._vm_base_manager.start():
            self.update_vm_local()
        else:
            g.error_code = 2041
            raise Exception('vm start failed')

    def stop(self, force=True):
        """
        虚拟机实例关机
        :parmas force:
        """
        if self._vm_base_manager.stop(force):
            self.update_vm_local()
        else:
            g.error_code = 2043
            raise Exception('vm stop failed')

    def suspend(self, force=True):
        """
        虚拟机实例暂停
        :params force:
        """
        if self._vm_base_manager.suspend(force):
            self.update_vm_local()
        else:
            g.error_code = 2045
            raise Exception('vm suspend failed')

    def restart(self):
        """
        虚拟机实例重启
        """
        if self._vm_base_manager.reboot():
            self.update_vm_local()
        else:
            raise Exception('vm restart failed')

    def delete(self):
        """
        虚拟机实例删除
        """
        if self._vm_base_manager.delete():
            self.update_vm_local()
        else:
            raise Exception('vm delete failed')

    def add_snapshot(self, snapshot_name, description, dumpMemory=False, quiesce=True):
        """
        添加快照
        :params snapshot_name:
        :params description:
        :params dumpMemory:
        :params quiesce:
        """
        if self._vm_snapshot_manager.create_snapshot(snapshot_name, description, dumpMemory, quiesce):
            snapshot_nanage.sync_snapshot(self.platform_id, self.vm)
        else:
            raise Exception('Add Snapshot Failed')

    def delete_snapshot(self, snapshot_id):
        """
        删除快照
        :params snapshot_id:
        """
        snapshot_db = snapshot_nanage.get_snapshot_by_snapshot_id(self.vm, snapshot_id)

        if not snapshot_db:
            raise Exception('')

        if self._vm_snapshot_manager.remove_snapshot(snapshot_db.name):
            snapshot_nanage.sync_snapshot(self.platform_id, self.vm)
        else:
            raise Exception('Delete Snapshot Failed')

    def snapshot_revert(self, snapshot_id):
        """
        恢复快照
        :params snapshot_id:
        """
        snapshot_db = snapshot_nanage.get_snapshot_by_snapshot_id(self.vm, snapshot_id)

        if not snapshot_db:
            g.error_code = 2304
            raise Exception('unable get snapshot info ')

        if self._vm_snapshot_manager.revert_snapshot(snapshot_db.name):
            snapshot_nanage.sync_snapshot(self.platform_id, self.vm)  # TODO 是否需要 原来部分没有
        else:
            g.error_code = 2304
            raise Exception('unable to find snapshot, revert failed')

    def boot(self, new_cpu, new_memory, dc_id, ds_id, vm_name, networks, disks, image_id):
        """
        创建主机
        :params new_cpu:
        :params new_memory:
        :params dc_id:
        :params ds_id:
        :params vm_name:
        :params networks:
        :params disks:
        :params image_id:
        """
        if disks:
            disk_data = json.loads(disks) if isinstance(disks, str) else disks
            for disk in disks:
                if not disk.get('type') or not disk.get('size'):
                    g.error_code = 2001
                    raise Exception('The disk information format is incorrect.')

        dc_info = db.vcenter.vcenter_tree_by_id(dc_id)
        # dc_name = dc_info.name
        if not dc_info:
            g.error_code = 2002
            raise Exception('The dc_id error')
        if self._vm_device_info_manager.build_without_device_info(vm_name, dc_info.dc_oc_name, int(new_cpu), int(new_memory)):
            self._set_vm(self._vm_device_info_manager.vm)
            self.update_vm_local()
        else:
            g.error_code = 2005
            raise Exception('Task To Create Failed')

        if networks:
            try:
                self.add_network(networks)
            except Exception as e:
                g.error_code = 2006
                raise Exception('vm network attach failed')

        if disks:
            try:
                self.add_disk(disks)
            except Exception as e:
                g.error_code = 2007
                raise Exception('vm disk attach failed')

        if image_id:
            try:
                self.add_image(image_id)
            except Exception as e:
                g.error_code = 2008
                raise Exception('vm image attach failed')

    def add_network(self, networks):
        """
        为当前主机添加网卡信息
        :params networks:
        """
        networks = json.loads(networks) if isinstance(networks, str) else networks

        for network in networks:
            local_network_port_group = network_port_group_manage.get_network_by_id(network)

            # TODO 创建单个网卡失败后要做什么
            if not self._vm_device_info_manager.add_network(local_network_port_group.name):
                raise Exception('Add Network Failed')

        # 同步云主机网卡信息
        sync_network_device(self.platform_id, self.vm)

    def del_network(self, networks):
        """
        删除网卡
        :params networks:
        """
        networks = json.loads(networks) if isinstance(networks, str) else networks

        for network_d_id in networks:
            device = network_device_manage.device_list_by_id(self.platform_id, self.uuid, network_d_id)
            if not device:
                g.error_code = 2211
                raise RuntimeError('Network Could Not Be Found')

            # TODO
            if not self._vm_device_info_manager.remove_network(device.label):
                g.error_code = 2212
                raise Exception('vm network delete failed')

        sync_network_device(self.platform_id, self.vm)

    def update_vcpu(self, new_cpu, old_cpu):
        """
        更新CPU信息
        :params new_cpu:
        :params old_cpu:
        """
        if self._vm_device_info_manager.update_vcpu(new_cpu):
            self.update_vm_local()
        else:
            g.error_code = 2021
            raise Exception('VM CPU Update Failed')

    def update_vmemory(self, new_memory, old_memory):
        """
        更新内存信息
        :params new_memory:
        :params old_memory:
        """
        if self._vm_device_info_manager.update_mem(new_memory):
            self.update_vm_local()
        else:
            g.error_code = 2022
            raise Exception('VM Memory Update Failed')

    def add_disk(self, disks):
        """
        添加磁盘信息
        :params disks:
        """
        disks = json.loads(disks) if isinstance(disks, str) else disks

        for disk in disks:
            if not disk.get('type'):
                g.error_code = 2001
                raise Exception('The disk information format is incorrect.')
            if not disk.get('size'):
                g.error_code = 2002
                raise Exception('The disk information format is incorrect.')

            if not self._vm_device_info_manager.add_disk(disk.get('size'), disk.get('type')):
                raise Exception('The disk information format is incorrect.')

        sync_disk(self.platform_id, self.vm)

    def delete_disk(self, disks, languag=None):
        """
        删除磁盘
        :params disks:
        :params languag:
        """
        disks = json.loads(disks) if isinstance(disks, str) else disks
        disk_id_list = sorted(disks, reverse=True)
        for disk_id in sorted(disks, reverse=True):
            disk = disk_manage.get_disk_by_disk_id(disk_id)
            if not disk:
                g.error_code = 2112
                raise RuntimeError('Hdd prefix label could not be found')

            # TODO
            if not self._vm_device_info_manager.remove_disk(disk.label):
                g.error_code = 2113
                raise Exception('Delete Disk Failed')

        sync_disk(self.platform_id, self.vm)

    def add_image(self, image_id):
        """
        添加镜像文件
        :params image_id:
        """
        image = db.images.get_image_by_image_id(image_id)
        if not image:
            raise RuntimeError('Image Id Could Not Be Found')

        if not self._vm_device_info_manager.add_image(image.path, image.ds_name):
            raise Exception('Add Image Failed')

    # 获取云主机列表
    def list(self, host, vm_name, pgnum, pgsort, template=None):
        try:
            vms, pg = db.instances.vm_list(self.platform_id, host, vm_name, pgnum, pgsort, template=template)
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

                    vm_temp['created_at'] = vm.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    vm_list.append(vm_temp)
        except Exception as e:
            raise Exception('vm list get failed')
        return vm_list, pg

    # 根据uuid 获取云主机信息
    def list_by_uuid(self, uuid):
        vm = db.instances.list_by_uuid(self.platform_id, uuid)
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

    # 同步云主机信息
    def update_vm_local(self):

        if self.vm.summary.guest is not None:
            ip = self.vm.summary.guest.ipAddress
        else:
            ip = ''

        if self.vm.resourcePool:
            resource_pool_name = self.vm.resourcePool.name
            # db.instances.update_vm_rp_name_by_vm_mor_name(platform['id'], get_mor_name(vm), vm.resourcePool.name)
        else:
            resource_pool_name = None

        vm = db.instances.list_by_uuid(uuid=self.uuid, platform_id=self.platform_id)
        if vm:
            db.instances.vcenter_update_vm_by_uuid(uuid=self.uuid, platform_id=self.platform_id,
                                                   vm_name=self.vm.summary.config.name,
                                                   vm_mor_name=get_mor_name(self.vm),
                                                   template=self.vm.summary.config.template,
                                                   vm_path_name=self.vm.summary.config.vmPathName,
                                                   memory=self.vm.summary.config.memorySizeMB,
                                                   cpu=self.vm.summary.config.numCpu,
                                                   num_ethernet_cards=self.vm.summary.config.numEthernetCards,
                                                   num_virtual_disks=self.vm.summary.config.numVirtualDisks,
                                                   instance_uuid=self.vm.summary.config.instanceUuid,
                                                   guest_id=self.vm.summary.config.guestId,
                                                   guest_full_name=self.vm.summary.config.guestFullName,
                                                   host=self.local_vm.host, ip=ip,
                                                   status=self.vm.summary.runtime.powerState,
                                                   resource_pool_name=resource_pool_name)
        else:
            db.instances.vcenter_vm_create(uuid=self.vm.summary.config.uuid, platform_id=self.platform_id,
                                           vm_name=self.vm.summary.config.name,
                                           vm_mor_name=get_mor_name(self.vm), template=self.vm.summary.config.template,
                                           vm_path_name=self.vm.summary.config.vmPathName,
                                           memory=self.vm.summary.config.memorySizeMB,
                                           cpu=self.vm.summary.config.numCpu,
                                           num_ethernet_cards=self.vm.summary.config.numEthernetCards,
                                           num_virtual_disks=self.vm.summary.config.numVirtualDisks,
                                           instance_uuid=self.vm.summary.config.instanceUuid,
                                           guest_id=self.vm.summary.config.guestId,
                                           guest_full_name=self.vm.summary.config.guestFullName,
                                           host='192.168.12.203', ip=ip, status=self.vm.summary.runtime.powerState,
                                           resource_pool_name=resource_pool_name, created_at=self.vm.config.createDate)

    def clone(self, new_vm_name, ds_id, dc_id=None, resourcepool=None):
        """
        克隆虚机
        :params new_vm_name:
        :params ds_id:
        :params dc_id:
        :params resourcepool:
        """
        try:
            ds_info = db.datastores.get_ds_by_id(ds_id)
            dc_info = db.vcenter.vcenter_tree_by_id(dc_id)
            if not ds_info:
                raise Exception('Unable to get DataStore')
        except Exception as e:
            g.error_code = 2051
            raise Exception('Unable to get DataStore or DataCenter')

        clone_status = self._vm_device_info_manager.clone(
            new_vm_name=new_vm_name,
            dc_name=validate_input(dc_info.dc_oc_name) if dc_info else None,
            ds_name=validate_input(ds_info.ds_name),
            rp_name=validate_input(resourcepool)
        )
        if not clone_status:
            g.error_code = 2054
            raise Exception("Perform a clone operation error")

    def cold_migrate(self, host_name=None, ds_id=None, dc_id=None, resourcepool=None):
        """
        冷迁移
        :params host_name:
        :params ds_id:
        :params dc_id:
        :params resourcepool:
        """
        old_name = self.vm.summary.config.name
        old_uuid = self.vm.summary.config.uuid

        vm_name_tmp = old_name + '_tmp'
        try:
            ds_info = db.datastores.get_ds_by_id(ds_id)
            dc_info = db.vcenter.vcenter_tree_by_id(dc_id)
        except Exception as e:
            g.error_code = 2061
            raise Exception('Unable to get DataStore or DataCenter')

        if not ds_info:
            raise Exception('Unable to get DataStore')

        clone_status = self._vm_device_info_manager.clone(
            new_vm_name=vm_name_tmp,

            dc_name=validate_input(dc_info.dc_oc_name) if dc_info else None,
            ds_name=validate_input(ds_info.ds_name),
            rp_name=validate_input(resourcepool),
            target_host_name=host_name
        )

        if clone_status:
            # TODO 相关操作还要归类
            if not self._vm_base_manager.delete():
                g.error_code = 2063
                raise Exception("cold migrate failed")

            try:
                vm_conf = vim.vm.ConfigSpec()
                vm_conf.name = old_name
                vm_conf.uuid = old_uuid

                cold_migrated_vm = self._vm_device_info_manager._get_device([vim.VirtualMachine], vm_name_tmp)
                WaitForTask(cold_migrated_vm.ReconfigVM_Task(vm_conf))
            except Exception as e:
                g.error_code = 2063
                raise Exception('cold migrate failed')

            self._set_vm(cold_migrated_vm)
        else:
            raise Exception('Perform a clone operation error')

    def ip_assignment(self, ip, subnet, gateway, dns, domain=None):
        try:

            vm = self.vm
            vm_name = vm.summary.config.name
            vm_name = vm_name.replace('_', '-')
            if vm.runtime.powerState != 'poweredOff':
                g.error_code = 2071
                raise Exception('Power off your VM before reconfigure')

            adaptermap = vim.vm.customization.AdapterMapping()
            globalip = vim.vm.customization.GlobalIPSettings()
            adaptermap.adapter = vim.vm.customization.IPSettings()

            adaptermap.adapter.ip = vim.vm.customization.FixedIp()
            adaptermap.adapter.ip.ipAddress = ip
            adaptermap.adapter.subnetMask = subnet
            adaptermap.adapter.gateway = gateway
            globalip.dnsServerList = dns
            if not domain:
                domain = 'kaopuyun.com'
            adaptermap.adapter.dnsDomain = domain

            # globalip = vim.vm.customization.GlobalIPSettings()
            # For Linux . For windows follow sysprep
            ident = vim.vm.customization.LinuxPrep(domain=domain,
                                                   hostName=vim.vm.customization.FixedName(name=vm_name))
            customspec = vim.vm.customization.Specification()
            # For only one adapter
            customspec.identity = ident
            customspec.nicSettingMap = [adaptermap]
            customspec.globalIPSettings = globalip

            # Configuring network for a single NIC
            # For multipple NIC configuration contact me.

            print "Reconfiguring VM Networks . . ."

            task = vm.Customize(spec=customspec)
            # Wait for Network Reconfigure to complete

            wait_for_tasks(self.si, [task])

        except vmodl.MethodFault, e:
            # print "Caught vmodl fault: %s" % e.msg
            g.error_code = 2071
            raise Exception('Caught vmodl fault: %s' % e.msg)
        except Exception, e:
            print "Caught exception: %s" % str(e)
            g.error_code = 2072
            raise Exception('Caught exception fault: %s' % str(e))

    def vm_transform_template(self):
        # MarkAsTemplate
        if self.vm:
            if not self.vm.summary.config.template:
                print ("Vm transform template...")
                self.vm.MarkAsTemplate()
                # 同步
                db.instances.vcenter_sync_vm_transform_template(self.platform_id, self.uuid)
            else:
                raise Exception('Object are not vm')
        else:
            raise ValueError('The vm does not exist.')

# def find_snapshot(snapshot, snapshot_name):
#     for snapshot in snapshot.childSnapshotList:
#         if snapshot.name == snapshot_name:
#             return snapshot
#         if hasattr(snapshot, "childSnapshotList"):
#             snap_obj = find_snapshot(snapshot, snapshot_name)
#             if snap_obj:
#                 return snap_obj


# def get_hdd_prefix_label(language):
#     language_prefix_label_mapper = {
#         'English': 'Hard disk ',
#         'Chinese': u'硬盘 '
#     }
#     return language_prefix_label_mapper.get(language)

