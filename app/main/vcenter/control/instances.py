# -*- coding:utf-8 -*-

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
import atexit

import json

from app.main.vcenter import db


class Instance(object):

    def __init__(self, platform_id, uuid=None, si=None, content=None, network_port_group=None, network_device=None):
        # print('platform_id:', platform_id)
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

            local_vm = db.instances.list_by_uuid(self.platform_id, self.uuid)
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
            self.update_vm_local()
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
            self.update_vm_local()
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
            self.update_vm_local()
        except Exception as e:
            raise Exception('vm suspend failed')

    # 重启
    def restart(self):
        task = self.vm.ResetVM_Task()
        wait_for_tasks(self.si, [task])
        self.update_vm_local()

    def delete(self):
        task = self.vm.Destroy()
        wait_for_tasks(self.si, [task])

    # 新增网卡信息
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
        # 同步云主机网卡信息
        sync_network_device(self.platform_id, self.vm)

    # 删除网卡信息
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
            # 同步云主机网卡信息
            sync_network_device(self.platform_id, self.vm)
        except Exception as e:
            Exception('vm network delete failed')

    # 更新cpu信息
    def update_vcpu(self, new_cpu, old_cpu):
        try:
            # if self.local_vm.cpu == old_cpu:
            cspec = vim.vm.ConfigSpec()
            cspec.numCPUs = int(new_cpu)
            cspec.numCoresPerSocket = 1
            task = self.vm.Reconfigure(cspec)
            wait_for_tasks(self.si, [task])
            self.update_vm_local()
            # else:
            #     raise Exception('参数错误')
        except Exception as e:
            raise Exception('vm cpu update failed')

    # 更新内存信息
    def update_vmemory(self, new_memory, old_memory):
        try:
            # if self.local_vm.memory == old_memory:
            print ('cccc')
            cspec = vim.vm.ConfigSpec()
            cspec.memoryMB = int(new_memory)
            task = self.vm.Reconfigure(cspec)
            wait_for_tasks(self.si, [task])
            self.update_vm_local()
            # else:
            #     raise Exception('参数错误')
        except Exception as e:
            raise Exception('vm memory update failed')

    # 创建云主机
    def boot(self, new_cpu, new_memory, dc_id, ds_id, vm_name, networks, disks, image_id):

        try:
            if disks:
                new_disks = json.loads(disks)
                for disk in new_disks:
                    if not disk.get('type'):
                        raise Exception('The disk information format is incorrect.')
                    if not disk.get('size'):
                        raise Exception('The disk information format is incorrect.')
        except Exception as e:
            raise Exception('The disk information format is incorrect.')

        try:

            dc_info = db.vcenter.vcenter_tree_by_id(dc_id)
            dc = get_obj(self.content, [vim.Datacenter], dc_info.name)
        except Exception as e:
            raise Exception('dc get failed')

        vm_folder = dc.vmFolder
        hosts = dc.hostFolder.childEntity
        resource_pool = hosts[0].resourcePool

        # ds = content.viewManager.CreateContainerView(dc, [vim.Datastore], True)

        ds = get_obj(self.content, [vim.Datastore], 'datastore1')

        # datastore_path = '[' + ds + '] ' + vm_name
        datastore_path = '[datastore1] ' + vm_name
        print datastore_path
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
        try:
            task = vm_folder.CreateVM_Task(config=config, pool=resource_pool)
            wait_for_tasks(self.si, [task])
            vm = get_obj(self.content, [vim.VirtualMachine], vm_name)
            self.vm = vm
            self.update_vm_local()
        except Exception as e:
            raise Exception('task to create failed')
        try:
            # 获取vm 并为vm 添加network

            if networks:
                self.add_network(networks)
        except Exception as e:
            raise Exception('vm network attach failed')
        try:
            if disks:
                self.add_disk(disks)
        except Exception as e:
            raise Exception('vm disk attach failed')
        try:
            if image_id:
                self.add_image(image_id)
            # vm_add_network(self.platform_id, vm.summary.config.uuid, networks, vm)
        except Exception as e:
            raise Exception('vm image attach failed')

    # 获取云主机列表
    def list(self, host, vm_name, pgnum, pgsort):
        try:
            vms, pg = db.instances.vm_list(self.platform_id, host, vm_name, pgnum, pgsort)
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
        print('vm1')
        if vm:
            print('update_vm')
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
            print('update_vm2')
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

    def add_disk(self, disks):
        print('disks:', disks)
        disks = json.loads(disks)

        controller = vim.vm.device.ParaVirtualSCSIController()
        controller.sharedBus = vim.vm.device.VirtualSCSIController.Sharing.noSharing
        virtual_device_spec = vim.vm.device.VirtualDeviceSpec()
        virtual_device_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        virtual_device_spec.device = controller
        config_spec = vim.vm.ConfigSpec()
        config_spec.deviceChange = [virtual_device_spec]
        task = self.vm.ReconfigVM_Task(config_spec)
        wait_for_tasks(self.si, [task])

        for disk in disks:
            print('disk:', disk)
            disk_size = disk.get('size')
            disk_type = disk.get('type')
            if not all([disk_size, disk_type]):
                raise Exception('parameter error')

            spec = vim.vm.ConfigSpec()
            # get all disks on a VM, set unit_number to the next available
            unit_number = 0
            for dev in self.vm.config.hardware.device:
                if hasattr(dev.backing, 'fileName'):
                    unit_number = int(dev.unitNumber) + 1
                    # unit_number 7 reserved for scsi controller
                    if unit_number == 7:
                        unit_number += 1
                    if unit_number >= 16:
                        print "we don't support this many disks"
                        raise Exception("we don't support this many disks")
                if isinstance(dev, vim.vm.device.VirtualSCSIController):
                    controller = dev

            # add disk here
            dev_changes = []
            new_disk_kb = int(disk_size) * 1024 * 1024
            disk_spec = vim.vm.device.VirtualDeviceSpec()
            disk_spec.fileOperation = "create"
            disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            disk_spec.device = vim.vm.device.VirtualDisk()
            disk_spec.device.backing = \
                vim.vm.device.VirtualDisk.FlatVer2BackingInfo()

            if disk_type == 'thin':
                disk_spec.device.backing.thinProvisioned = True

            disk_spec.device.backing.diskMode = 'persistent'
            disk_spec.device.unitNumber = unit_number
            disk_spec.device.capacityInKB = new_disk_kb
            disk_spec.device.controllerKey = controller.key
            dev_changes.append(disk_spec)
            spec.deviceChange = dev_changes
            print(1)
            task = self.vm.ReconfigVM_Task(spec=spec)
            wait_for_tasks(self.si, [task])

        sync_disk(self.platform_id, self.vm)

    def delete_disk(self, disks, languag=None):
        language = 'English'

        # disks = json.loads(disks)
        for disk_id in disks:

            # 获取根据云盘id 获取 disk 信息
            disk = disk_manage.get_disk_by_disk_id(disk_id)
            print (disk)
            hdd_prefix_label = disk.label
            # hdd_prefix_label = get_hdd_prefix_label(language)
            if not hdd_prefix_label:
                raise RuntimeError('Hdd prefix label could not be found')

            # hdd_label = hdd_prefix_label + str(disk_number)
            # hdd_label = hdd_prefix_label + str(4)
            virtual_hdd_device = None
            for dev in self.vm.config.hardware.device:
                if isinstance(dev, vim.vm.device.VirtualDisk) \
                        and dev.deviceInfo.label == hdd_prefix_label:
                    virtual_hdd_device = dev
            if not virtual_hdd_device:
                raise RuntimeError('Virtual {} could not '
                                   'be found.'.format(virtual_hdd_device))

            virtual_hdd_spec = vim.vm.device.VirtualDeviceSpec()
            virtual_hdd_spec.operation = \
                vim.vm.device.VirtualDeviceSpec.Operation.remove
            virtual_hdd_spec.device = virtual_hdd_device

            spec = vim.vm.ConfigSpec()
            spec.deviceChange = [virtual_hdd_spec]
            task = self.vm.ReconfigVM_Task(spec=spec)
            wait_for_tasks(self.si, [task])
        sync_disk(self.platform_id, self.vm)

    # 添加iso文件
    def add_image(self, image_id):
        image = db.images.get_image_by_image_id(image_id)
        # ds = image_path.split(']')
        # datastore_name = ds[0][1:]
        image_path = image.path
        datastore_name = image.ds_name

        # content = service_instance.RetrieveContent()
        controller = vim.vm.device.VirtualIDEController()
        for dev in self.vm.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualIDEController):
                controller = dev

        cdspec = None
        cdspec = vim.vm.device.VirtualDeviceSpec()
        cdspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        cdspec.device = vim.vm.device.VirtualCdrom()
        cdspec.device.key = 3000
        cdspec.device.controllerKey = controller.key

        # unit number == ide controller slot, 0 is first ide disk, 1 second
        cdspec.device.unitNumber = 0
        cdspec.device.deviceInfo = vim.Description()
        cdspec.device.deviceInfo.label = 'CD/DVD drive 1'
        cdspec.device.deviceInfo.summary = 'ISO'
        cdspec.device.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo()
        cdspec.device.backing.fileName = image_path
        datastore = get_obj(content=self.content, vimtype=[vim.Datastore], name=datastore_name)
        cdspec.device.backing.datastore = datastore
        # cdspec.device.backing.dynamicType =
        # cdspec.device.backing.backingObjectId = '0'
        cdspec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        cdspec.device.connectable.startConnected = True
        cdspec.device.connectable.allowGuestControl = True
        cdspec.device.connectable.connected = False
        cdspec.device.connectable.status = 'untried'
        vmconf = vim.vm.ConfigSpec()
        vmconf.deviceChange = [cdspec]
        dev_changes = []
        dev_changes.append(cdspec)
        vmconf.deviceChange = dev_changes
        task = self.vm.ReconfigVM_Task(spec=vmconf)
        wait_for_tasks(self.si, [task])

    def add_snapshot(self, snapshot_name, description):
        dumpMemory = False
        quiesce = True
        task = self.vm.CreateSnapshot(snapshot_name, description, dumpMemory, quiesce)
        wait_for_tasks(self.si, [task])
        snapshot_nanage.sync_snapshot(self.platform_id, self.vm)

    def delete_snapshot(self, snapshot_id):
        snapshots = self.vm.snapshot.rootSnapshotList
        snapshot_db = snapshot_nanage.get_snapshot_by_snapshot_id(self.vm, snapshot_id)

        snapshot_name = snapshot_db.name

        for snapshot in snapshots:
            if snapshot_name == snapshot.name:

                snap_obj = snapshot.snapshot

                task = snap_obj.RemoveSnapshot_Task(True)
                wait_for_tasks(self.si, [task])

            else:
                if len(snapshot.childSnapshotList) > 0:
                    snap_obj = find_snapshot(snapshot, snapshot_name)
                    task = snap_obj.snapshot.RemoveSnapshot_Task(True)
                    wait_for_tasks(self.si, [task])
        snapshot_nanage.sync_snapshot(self.platform_id, self.vm)

    def snapshot_revert(self, snapshot_id):
        snapshots = self.vm.snapshot.rootSnapshotList
        snapshot_db = snapshot_nanage.get_snapshot_by_snapshot_id(self.vm, snapshot_id)
        if snapshot_db:
            raise Exception('unable get snapshot info ')
        snapshot_name = snapshot_db.name
        # print(snapshot_name)
        for snapshot in snapshots:
            print(snapshot.name)
            if snapshot_name == snapshot.name:

                snap_obj = snapshot.snapshot
                task = snap_obj.RevertToSnapshot_Task()
                wait_for_tasks(self.si, [task])

            else:
                if len(snapshot.childSnapshotList) > 0:

                    snap_obj = find_snapshot(snapshot, snapshot_name)
                    if snap_obj:
                        task = snap_obj.snapshot.RevertToSnapshot_Task()
                        wait_for_tasks(self.si, [task])
                    else:
                        raise Exception('unable to find snapshot,revert failed')
                else:
                    raise Exception('unable to find snapshot,revert failed')

    def clone(self, new_vm_name, ds_id, dc_id=None, resourcepool=None):
        template = self.vm.summary.config.name
        try:
            ds = db.datastores.get_ds_by_id(ds_id)
            dc = db.vcenter.vcenter_tree_by_id(dc_id)
        except Exception as e:
            raise Exception('Unable to get DataStore or DataCenter')
        if dc:
            datacenter = get_obj(self.content, [vim.Datacenter], validate_input(dc.name))
        else:
            datacenter = self.content.rootFolder.childEntity[0]

        vmfolder = datacenter.vmFolder
        hosts = datacenter.hostFolder.childEntity

        relospec = vim.vm.RelocateSpec()
        if ds:
            datastore = get_obj(self.content, [vim.Datastore], validate_input(ds.ds_name))
            if datastore:
                # print "Using datastore " + validate_input(ds)
                relospec.datastore = datastore
            else:
                raise Exception('Unable to get DataStore')
        else:
            raise Exception('Unable to get DataStore')
        if resourcepool:
            resource_pool = get_obj(self.content, [vim.ResourcePool], validate_input(resourcepool))
        else:

            resource_pool = hosts[0].resourcePool
        # resource_pool = cluster.resourcePool
        if resource_pool:
            relospec.pool = resource_pool
        else:
            print "Cloud not find resource pool, using resource pool of origin VM"

        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec
        clonespec.powerOn = False

        template = get_obj(self.content, [vim.VirtualMachine], validate_input(template))
        if not template:
            # print "VM or template not found"
            raise Exception('VM or template not found')
        try:
            task = template.Clone(folder=vmfolder, name=validate_input(new_vm_name),
                                  spec=clonespec, )

            wait_for_tasks(self.si, [task])

        except Exception as e:
            raise Exception('Perform a clone operation error')

    def cold_migrate(self, host_name=None, ds_id=None, dc_id=None, resourcepool=None):
        vm_name_tmp = self.vm.summary.config.name + '_tmp'

        template = self.vm.summary.config.name
        try:
            ds = db.datastores.get_ds_by_id(ds_id)
            dc = db.vcenter.vcenter_tree_by_id(dc_id)
        except Exception as e:
            raise Exception('Unable to get DataStore or DataCenter')
        if dc:
            datacenter = get_obj(self.content, [vim.Datacenter], validate_input(dc.name))
        else:
            datacenter = self.content.rootFolder.childEntity[0]
        vmfolder = datacenter.vmFolder
        clusters = datacenter.hostFolder.childEntity

        target_cluster = None
        for cluster in clusters:

            for host in cluster.host:
                if host.name == host_name:
                    target_cluster = cluster
                    break

        relospec = vim.vm.RelocateSpec()
        if ds:
            datastore = get_obj(self.content, [vim.Datastore], validate_input(ds.ds_name))
            if datastore:
                # print "Using datastore " + validate_input(ds)
                relospec.datastore = datastore
            else:
                raise Exception('Unable to get DataStore')
        else:
            raise Exception('Unable to get DataStore')
        if resourcepool:
            resource_pool = get_obj(self.content, [vim.ResourcePool], validate_input(resourcepool))
        else:

            resource_pool = target_cluster.resourcePool
        # resource_pool = cluster.resourcePool
        if resource_pool:
            relospec.pool = resource_pool
        else:
            print "Cloud not find resource pool, using resource pool of origin VM"

        target_host = get_obj(self.content, [vim.HostSystem], host_name)

        # relocate_spec = vim.vm.RelocateSpec()
        # for datastore in target_host.datastore:
        #     # Store the OVS vApp VM in local datastore of each host
        #     if datastore.summary.type == 'VMFS':
        #         print " Moving the VM in %s" % datastore.name
        #         relocate_spec.datastore = datastore
        #         break

        # relospec.host = target_host

        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec
        clonespec.powerOn = False

        # template = get_obj(self.content, [vim.VirtualMachine], validate_input(template))
        # if not template:
        #     # print "VM or template not found"
        #     raise Exception('VM or template not found')
        try:

            task = self.vm.Clone(folder=vmfolder, name=vm_name_tmp,
                                 spec=clonespec)

            wait_for_tasks(self.si, [task])

            vmconf = vim.vm.ConfigSpec()
            vmconf.name = self.vm.summary.config.name
            vmconf.uuid = self.vm.summary.config.uuid

            print "Destroying the source VM"
            task = self.vm.Destroy()

            # wait_for_task(task, si)
            wait_for_tasks(self.si, [task])
            print "Configuring the VM with old name and uuid"

            new_vm = get_obj(self.content, [vim.VirtualMachine], vm_name_tmp)

            task = new_vm.ReconfigVM_Task(vmconf)
            wait_for_tasks(self.si, [task])

            # relocate_spec = vim.vm.RelocateSpec(host=target_host)
            # task = new_vm.Relocate(relocate_spec)
            # wait_for_tasks(self.si, [task])

            print "Successfully cold migrated"

        except Exception as e:
            raise Exception('cold migrate failed')

    def ip_assignment(self, ip, subnet, gateway, dns, domain=None):
        try:

            vm = self.vm
            vm_name = vm.summary.config.name
            if vm.runtime.powerState != 'poweredOff':
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

            globalip = vim.vm.customization.GlobalIPSettings()
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
            raise Exception('Caught vmodl fault: %s' % e.msg)
        except Exception, e:
            print "Caught exception: %s" % str(e)
            raise Exception('Caught exception fault: %s' % str(e))


def find_snapshot(snapshot, snapshot_name):
    for snapshot in snapshot.childSnapshotList:
        if snapshot.name == snapshot_name:
            return snapshot
        if hasattr(snapshot, "childSnapshotList"):
            snap_obj = find_snapshot(snapshot, snapshot_name)
            if snap_obj:
                return snap_obj


def get_hdd_prefix_label(language):
    language_prefix_label_mapper = {
        'English': 'Hard disk ',
        'Chinese': u'硬盘 '
    }
    return language_prefix_label_mapper.get(language)
