# -*- coding:utf-8 -*-
from flask import g

from app.main.vcenter.control.utils import get_mor_name, wait_for_tasks, get_obj, get_connect, validate_input
from app.main.vcenter.control.disks import sync_disk
from app.main.vcenter.control.network_devices import sync_network_device

from app.main.base import control as base_control

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
        if not self.local_vm:
            g.error_code = 3993
            raise Exception("Get local VM Failed")
        
        data = dict(
            type='vm_control',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('虚拟机({})开机'.format(self.local_vm.id)),
            submitter=g.username,
        )

        status, info = self._vm_base_manager.start()
        if status:
            g.error_code = 3000
            self.update_vm_local()
            data['result'] = True
            base_control.event_logs.eventlog_create(**data)  # 信息记录
        else:
            g.error_code = 3001
            base_control.event_logs.eventlog_create(**data)
            raise Exception(info)

    def stop(self, force=True):
        """
        虚拟机实例关机
        :parmas force:
        """
        if not self.local_vm:
            g.error_code = 3993
            raise Exception("Get local VM Failed")
        
        data = dict(
            type='vm_control',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('虚拟机({})关机'.format(self.local_vm.id)),
            submitter=g.username,
        )

        status, info = self._vm_base_manager.stop(force)
        if status:
            g.error_code = 3020
            self.update_vm_local()  # 同步
            data['result'] = True
            base_control.event_logs.eventlog_create(**data)  # 信息记录
        else:
            g.error_code = 3021
            base_control.event_logs.eventlog_create(**data)  # 信息记录
            raise Exception(info.msg)

    def suspend(self, force=True):
        """
        虚拟机实例暂停
        :params force:
        """
        if not self.local_vm:
            g.error_code = 3993
            raise Exception("Get local VM Failed")
        
        data = dict(
            type='vm_control',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('虚拟机({})挂起'.format(self.local_vm.id)),
            submitter=g.username,
        )
        status, info = self._vm_base_manager.suspend(force)
        if status:
            g.error_code = 3040
            self.update_vm_local()
            data['result'] = True
            base_control.event_logs.eventlog_create(**data)  # 信息记录
        else:
            g.error_code = 3041
            base_control.event_logs.eventlog_create(**data)  # 信息记录
            raise Exception(info.msg)

    def restart(self):
        """
        虚拟机实例重启
        """
        if not self.local_vm:
            g.error_code = 3993
            raise Exception("Get local VM Failed")
        
        data = dict(
            type='vm_control',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('虚拟机({})重启'.format(self.local_vm.id)),
            submitter=g.username,
        )

        status, info = self._vm_base_manager.reboot()
        if status:
            g.error_code = 3060
            self.update_vm_local()
            data['result'] = True
            base_control.event_logs.eventlog_create(**data)  # 信息记录
        else:
            g.error_code = 3061
            base_control.event_logs.eventlog_create(**data)  # 信息记录
            raise Exception(info.msg)

    def delete(self):
        """
        虚拟机实例删除
        """
        if not self.local_vm:  # 无本地数据 认为错误
            g.error_code = 3993
            raise Exception("Get local VM Failed")
        
        data = dict(
            type='vm_control',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('删除虚拟机: {}'.format(self.local_vm.id)),
            submitter=g.username,
        )

        status, info = self._vm_base_manager.delete()
        if status:
            g.error_code = 3080
            self.update_vm_local()  # VM同步
            data['result'] = True
            base_control.event_logs.eventlog_create(**data)  # 信息记录
        else:
            g.error_code = 3081
            base_control.event_logs.eventlog_create(**data)
            raise Exception(info.msg)            

    def add_snapshot(self, snapshot_name, description, dumpMemory=False, quiesce=True):
        """
        添加快照
        :params snapshot_name:
        :params description:
        :params dumpMemory:
        :params quiesce:
        """
        status, info = self._vm_snapshot_manager.create_snapshot(snapshot_name, description, dumpMemory, quiesce)
        if status:
            g.error_code = 3150
            snapshot_nanage.sync_snapshot(self.platform_id, self.vm)
        else:
            g.error_code = 3151
            raise Exception(info.msg)

    def delete_snapshot(self, snapshot_id):
        """
        删除快照
        :params snapshot_id:
        """
        snapshot_db = snapshot_nanage.get_snapshot_by_snapshot_id(self.vm, snapshot_id)

        if not snapshot_db:
            g.error_code = 3182
            raise Exception('No corresponding snapshot was found')

        status, info = self._vm_snapshot_manager.remove_snapshot(snapshot_db.name)
        if status:
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
        # 校验创建的磁盘信息
        if disks:
            disk_data = json.loads(disks) if isinstance(disks, str) else disks
            for disk in disks:
                if not disk.get('type') or not disk.get('size'):
                    g.error_code = 3332
                    raise Exception('The disk information format is incorrect.')

        # 获取数据中心内容
        dc_info = db.vcenter.vcenter_tree_by_id(dc_id)
        if not dc_info:
            g.error_code = 3292
            raise Exception('No corresponding DataCenter data')

        build_data = dict(
            type='vm_hardware_boot',
            result=False,
            resources_id='',
            event=unicode('创建虚拟机: {}'.format(vm_name)),
            submitter=g.username,
        )
        # 创建vm实例
        build_status, build_info = self._vm_device_info_manager.build_without_device_info(
            vm_name, dc_info.dc_oc_name, int(new_cpu), int(new_memory))
        
        if build_status:
            g.error_code = 3290
            self._set_vm(self._vm_device_info_manager.vm)   # 设置vm对象为下一步处理
            self.update_vm_local()  # 同步
            self.local_vm = db.instances.list_by_uuid(self.platform_id, self.vm.config.uuid)  # 更新local_vm对象数据
            build_data['result'] = True
            build_data['resources_id'] = self.local_vm.id
            base_control.event_logs.eventlog_create(**build_data)
        else:
            g.error_code = 3291
            base_control.event_logs.eventlog_create(**build_data)
            raise Exception(build_info.msg)

        if networks:
            self.add_network(networks)

        if disks:    
            self.add_disk(disks)

        if image_id:
            self.add_image(image_id)
        
        self.update_vm_local()  # 同步
        g.error_code = 3290  # 避免分步动作对错误码的影响

    def add_network(self, networks):
        """
        为当前主机添加网卡信息
        :params networks:
        """
        data = dict(
            type='vm_hardware_network_driver',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('为虚拟机({})添加网卡信息'.format(self.local_vm.id)),
            submitter=g.username,
        )

        networks = json.loads(networks) if isinstance(networks, str) else networks
        
        if not isinstance(networks, dict):
            raise RuntimeError("Parameter Error!!!")

        # 添加Dvswitch 网络信息
        for network in networks.get('dvswitch', []):
            local_network_port_group = network_port_group_manage.get_dvs_network_by_id(network)
            network_status, network_info = self._vm_device_info_manager.add_network_dvswitch(local_network_port_group.name)

            if not network_status:
                g.error_code = 3311
                data["result"] = False
                data['event'] = unicode('为虚拟机({})添加DVS网卡信息'.format(self.local_vm.id))
                base_control.event_logs.eventlog_create(**data)
                raise Exception(network_info)
            
            data['result'] = True
            data['event'] = unicode('为虚拟机({})添加DVS网卡信息: {}'.format(self.local_vm.id, local_network_port_group.name))
            base_control.event_logs.eventlog_create(**data)  # 逐条记录

        # 添加Vswitch 网络信息
        for network in networks.get('vswitch', []):
            local_network_port_group = network_port_group_manage.get_network_by_id(network)

            network_status, network_info = self._vm_device_info_manager.add_network_vswitch(local_network_port_group.name)
            
            if not network_status:
                g.error_code = 3311  # TODO
                data['result'] = False
                data['event'] = unicode('为虚拟机({})添加VS网卡信息'.format(self.local_vm.id))
                base_control.event_logs.eventlog_create(**data)
                raise Exception(network_info)
            
            data['result'] = True
            data['event'] = unicode('为虚拟机({})添加VS网卡信息: {}'.format(self.local_vm.id, local_network_port_group.name))
            base_control.event_logs.eventlog_create(**data)  # 逐条记录

        # 同步云主机网卡信息
        sync_network_device(self.platform_id, self.vm)
        g.error_code = 3310

    def del_network(self, networks):
        """
        删除网卡
        :params networks:
        """
        networks = json.loads(networks) if isinstance(networks, str) else networks

        for network_d_id in networks:
            device = network_device_manage.device_list_by_id(self.platform_id, self.uuid, network_d_id)
            if not device:
                g.error_code = 3372
                raise RuntimeError('Local no corresponding network card information')

            # TODO
            network_status, network_info = self._vm_device_info_manager.remove_network(device.label)
            if not network_status:
                g.error_code = 3371
                raise Exception(network_info)

        sync_network_device(self.platform_id, self.vm)
        g.error_code = 3370

    def update_vcpu(self, new_cpu, old_cpu):
        """
        更新CPU信息
        :params new_cpu:
        :params old_cpu:
        """
        if not self.local_vm:  # 无本地数据 认为错误
            g.error_code = 3993
            raise Exception("Get local VM Failed")
        
        data = dict(  # 事件信息
            type='vm_hardware_VCPU',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('更新虚拟机CPU信息, {}'.format(new_cpu)),
            submitter=g.username,
        )

        status, info = self._vm_device_info_manager.update_vcpu(new_cpu)
        if status:
            g.error_code = 3410
            self.update_vm_local()  # 更新
            data['result'] = True
            base_control.event_logs.eventlog_create(**data)  # 事件记录
        else:
            g.error_code = 3411
            base_control.event_logs.eventlog_create(**data)
            raise Exception(info)

    def update_vmemory(self, new_memory, old_memory):
        """
        更新内存信息
        :params new_memory:
        :params old_memory:
        """
        if not self.local_vm:  # 无本地数据 认为错误
            g.error_code = 3993
            raise Exception("Get local VM Failed")
        
        data = dict(  # 事件信息
            type='vm_hardware_VMemory',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('更新虚拟机内存信息, {}'.format(new_memory)),
            submitter=g.username,
        )

        status, info = self._vm_device_info_manager.update_mem(new_memory)
        if status:
            g.error_code = 3430
            self.update_vm_local()
            data['result'] = True
            base_control.event_logs.eventlog_create(**data)  # 事件记录
        else:
            g.error_code = 3431
            base_control.event_logs.eventlog_create(**data)  # 事件记录
            raise Exception(info)

    def add_disk(self, disks):
        """
        添加磁盘信息
        :params disks:
        """
        data = dict(
            type='vm_hardware_disk',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('为虚拟机({})添加磁盘信息'.format(self.local_vm.id)),
            submitter=g.username,
        )

        disks = json.loads(disks) if isinstance(disks, str) else disks

        for disk in disks:   # TODO  整理代码 没必要这么多的处理
            if not disk.get('type'):
                g.error_code = 3333
                data['result'] = False
                data['event'] = unicode('为虚拟机({})添加磁盘信息, 磁盘类型: {}'.format(self.local_vm.id, disk.get('type')))
                base_control.event_logs.eventlog_create(**data)
                raise Exception('Input disk type')
            if not disk.get('size'):
                g.error_code = 3334
                data['result'] = False
                data['event'] = unicode('为虚拟机({})添加磁盘信息, 磁盘大小: {}'.format(self.local_vm.id, disk.get('size')))
                base_control.event_logs.eventlog_create(**data)
                raise Exception('Input disk size')

            disk_status, disk_info = self._vm_device_info_manager.add_disk(disk.get('size'), disk.get('type'))
            if not disk_status:
                g.error_code = 3331   # TODO
                data['result'] = False
                data['event'] = ('为虚拟机({})添加磁盘信息'.format(self.local_vm.id))
                base_control.event_logs.eventlog_create(**data)
                raise Exception(disk_info.msg)

            data['result'] = True
            data['event'] = unicode('为虚拟机({})添加磁盘信息: 类型={}, 大小={}'.format(self.local_vm.id, disk['type'], disk['size']))
            base_control.event_logs.eventlog_create(**data)  # 逐条记录

        sync_disk(self.platform_id, self.vm)
        g.error_code = 3330

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
        data = dict(
            type='vm_hardware_image',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('为虚拟机({})添加ISO文件'.format(self.local_vm.id)),
            submitter=g.username,
        )

        image = db.images.get_image_by_image_id(image_id)
        if not image:
            g.error_code = 3352
            base_control.event_logs.eventlog_create(**data)
            raise RuntimeError('No Specified Mirror Information')

        image_status, image_info = self._vm_device_info_manager.add_image(image.path, image.ds_name)
        if not image_status:
            g.error_code = 3351
            base_control.event_logs.eventlog_create(**data)
            raise Exception(image_info.msg)
        
        g.error_code = 3350
        data['result'] = True
        data['event'] = unicode('为虚拟机({})添加ISO文件: {}'.format(self.local_vm.id, image.iso_name))
        base_control.event_logs.eventlog_create(**data)

    # 获取云主机列表
    def list(self, host, vm_name, pgnum, pgsort, template=None):
        data = dict(
            type='vm',
            result=True,
            resources_id=None,
            event=unicode("获取云主机列表"),
            submitter=g.username,
        )

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
            g.error_code = 3551
            data['result'] = False
            raise Exception('Failed to obtain host list information')
        finally:
            base_control.event_logs.eventlog_create(**data)
        g.error_code = 3550
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
        if not self.local_vm:
            g.error_code = 3993
            raise Exception("Get local VM Failed")
        
        data = dict(
            type='vm_clone',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('克隆虚拟机({})'.format(self.local_vm.id)),
            submitter=g.username,
        )

        try:
            ds_info = db.datastores.get_ds_by_id(ds_id)
            dc_info = db.vcenter.vcenter_tree_by_id(dc_id)
            if not ds_info:
                raise Exception('Unable to get DataStore')
        except Exception as e:
            g.error_code = 3574
            base_control.event_logs.eventlog_create(**data)
            raise Exception('Unable to get DataStore or DataCenter')

        clone_status, info = self._vm_device_info_manager.clone(
            new_vm_name=new_vm_name,
            dc_name=validate_input(dc_info.dc_oc_name) if dc_info else None,
            ds_name=validate_input(ds_info.ds_name),
            rp_name=validate_input(resourcepool)
        )
        if not clone_status:
            g.error_code = 3571
            base_control.event_logs.eventlog_create(**data)
            raise Exception(info)
        
        g.error_code = 3570
        data['result'] = True
        base_control.event_logs.eventlog_create(**data)

    def cold_migrate(self, host_name=None, ds_id=None, dc_id=None, resourcepool=None):
        """
        冷迁移
        :params host_name:
        :params ds_id:
        :params dc_id:
        :params resourcepool:
        """
        if not self.local_vm:
            g.error_code = 3993
            raise Exception("Get local VM Failed")
        
        data = dict(
            type='vm_migrate',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('冷迁移虚拟机({})'.format(self.local_vm.id)),
            submitter=g.username,
        )

        old_name = self.vm.summary.config.name
        old_uuid = self.vm.summary.config.uuid

        vm_name_tmp = old_name + '_tmp'
        try:
            ds_info = db.datastores.get_ds_by_id(ds_id)
            dc_info = db.vcenter.vcenter_tree_by_id(dc_id)
            if not ds_info:
                raise Exception('Unable to get DataStore')
        except Exception as e:
            g.error_code = 3602
            base_control.event_logs.eventlog_create(**data)
            raise Exception('Query DS or DC failed')

        clone_status, info = self._vm_device_info_manager.clone(
            new_vm_name=vm_name_tmp,

            dc_name=validate_input(dc_info.dc_oc_name) if dc_info else None,
            ds_name=validate_input(ds_info.ds_name),
            rp_name=validate_input(resourcepool),
            target_host_name=host_name
        )

        if clone_status:
            # TODO 相关操作还要归类
            data['result'] = True
            base_control.event_logs.eventlog_create(**data)

            data['event'] = unicode("删除旧镜像")
            status, info = self._vm_base_manager.delete()
            if not status:
                g.error_code = 3603
                data['result'] = False
                base_control.event_logs.eventlog_create(**data)
                raise Exception(info.msg)

            base_control.event_logs.eventlog_create(**data)

            data['event'] = unicode("更新迁移后镜像名称")
            try:
                vm_conf = vim.vm.ConfigSpec()
                vm_conf.name = old_name
                vm_conf.uuid = old_uuid

                cold_migrated_vm = self._vm_device_info_manager._get_device([vim.VirtualMachine], vm_name_tmp)
                WaitForTask(cold_migrated_vm.ReconfigVM_Task(vm_conf))
                base_control.event_logs.eventlog_create(**data)
            except Exception as e:
                g.error_code = 3601
                data['result'] = False
                base_control.event_logs.eventlog_create(**data)
                raise Exception('Failure of cold migration')

            self._set_vm(cold_migrated_vm)
            self.update_vm_local()   # 更新
            g.error_code = 3600
        else:
            g.error_code = 3601
            base_control.event_logs.eventlog_create(**data)
            raise Exception(info)

    def ip_assignment(self, ip, subnet, gateway, dns, domain=None):
        data = dict(
            type='vm_ip_assignment',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('虚拟机({})IP分配'.format(self.local_vm.id)),
            submitter=g.username,
        )

        try:
            vm = self.vm
            vm_name = vm.summary.config.name
            vm_name = vm_name.replace('_', '-')
            if vm.runtime.powerState != 'poweredOff':
                g.error_code = 3632
                raise Exception('The machine is still on')

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
            data['result'] = True
            base_control.event_logs.eventlog_create(**data)
            g.error_code = 3630
        except vmodl.MethodFault, e:
            # print "Caught vmodl fault: %s" % e.msg
            g.error_code = 3633
            base_control.event_logs.eventlog_create(**data)
            raise Exception('Caught vmodl fault: %s' % e.msg)
        except Exception, e:
            print "Caught exception: %s" % str(e)
            g.error_code = 3631
            base_control.event_logs.eventlog_create(**data)
            raise Exception('Caught exception fault: %s' % str(e))

    def vm_transform_template(self):
        # MarkAsTemplate
        data = dict(
            type='vm_template',
            result=False,
            resources_id=self.local_vm.id,
            event=unicode('虚拟机({})转换为模板'.format(self.local_vm.id)),
            submitter=g.username,
        )

        if self.vm:
            if not self.vm.summary.config.template:
                print ("Vm transform template...")
                self.vm.MarkAsTemplate()
                # 同步
                db.instances.vcenter_sync_vm_transform_template(self.platform_id, self.uuid)
                g.error_code = 3360
                data['result'] = True
                base_control.event_logs.eventlog_create(**data)
            else:
                g.error_code = 3362
                base_control.event_logs.eventlog_create(**data)
                raise Exception('Object are not vm')
        else:
            g.error_code = 3363
            base_control.event_logs.eventlog_create(**data)
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

