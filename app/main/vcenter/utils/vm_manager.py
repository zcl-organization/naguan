# -*- coding:utf-8 -*-
"""
TODO 异常处理
"""
from pyVmomi import vim
from pyVmomi import vmodl
from pyVim.task import WaitForTask


class VMMaintainBaseManager:
    """虚拟机单机维护调度处理类"""

    def __init__(self, vm):
        self._vm = vm
    
    def start(self):
        """开机"""
        try:
            task = self._vm.PowerOn()
            WaitForTask(task)
        except Exception as e:
            return False, e
        
        return True, None
    
    def stop(self, force=True):
        """关机"""
        try:
            task = self._vm.ShutdownGuest() if not force else self._vm.PowerOff()
            WaitForTask(task)
        except Exception as e:
            return False, e
        
        return True, None
    
    def suspend(self, force=True):
        """暂停"""
        try:
            task = self._vm.StandbyGuest() if not force else self._vm.Suspend()
            WaitForTask(task)
        except Exception as e:
            return False, e
        
        return True, None
    
    def reboot(self):
        """重启"""
        try:
            task = self._vm.ResetVM_Task()
            WaitForTask(task)
        except Exception as e:
            return False, e
        
        return True, None
    
    def delete(self):
        """删除"""
        try:
            task = self._vm.Destroy()  # Destroy_Task()
            WaitForTask(task)
            self._vm = None
        except Exception as e:
            return False, e
        
        return True, None
    
    def rename(self, new_name):
        """重命名"""
        try:
            task = self._vm.Rename(new_name)
            WaitForTask(task)
        except Exception as e:
            return False, e
        
        return True, None

    def vm_info(self):
        """获取虚拟机信息"""
        if self._vm:
            return {
                'name': self._vm.name,
                'power_state': self._vm.runtime.powerState
            }
        else:
            raise ValueError("No VM Instance!!!")


class VMMaintainSnapshotManager:
    """虚拟机单机快照维护调度处理类"""

    def __init__(self, vm):
        self._vm = vm

    def snapshot_infos(self):
        """获取当前机器拥有的所有快照信息"""
        if self._vm.snapshot:
            return self._list_snapshots(self._vm.snapshot.rootSnapshotList)
        else:
            return []

    def create_snapshot(self, snapshot_name, snapshot_description, dumpMemory=False, quiesce=True):
        """创建快照"""
        try:
            task = self._vm.CreateSnapshot(snapshot_name, snapshot_description, dumpMemory, quiesce)
            WaitForTask(task)
        except Exception as e:
            return False, e

        return True, None

    def remove_snapshot(self, snapshot_name):
        """删除某个名称快照"""
        try:
            snap_objs = self._get_snapshots_by_name(self._vm.snapshot.rootSnapshotList, snapshot_name)
            if len(snap_objs) != 1:
                return False, ''
            
            task = snap_objs[0].snapshot.RemoveSnapshot_Task(True)
            WaitForTask(task)
        except Exception as e:
            return False, e.msg
        
        return True, None

    def revert_snapshot(self, snapshot_name):
        """还原某个名称快照"""
        try:
            snap_objs = self._get_snapshots_by_name(self._vm.snapshot.rootSnapshotList, snapshot_name)
            if len(snap_objs) != 1:
                return False
            
            task = snap_objs[0].snapshot.RevertToSnapshot_Task()
            WaitForTask(task)
        except Exception as e:
            return False
        
        return True

    def remove_all_snapshots(self):
        """删除当前虚拟机中的所有快照"""
        try:
            task = self._vm.RemoveAllSnapshots()
            WaitForTask(task)
        except Exception as e:
            return False
        
        return True
    
    def _get_snapshots_by_name(self, snapshots, snap_name):
        """通过名称查找快照"""
        snap_objs = []

        for snapshot in snapshots:
            if snapshot.name == snap_name:
                snap_objs.append(snapshot)
            elif len(snapshot.childSnapshotList) > 0:
                snap_objs = snap_objs + self._get_snapshots_by_name(snapshot.childSnapshotList, snap_name)

        return snap_objs

    def _list_snapshots(self, snapshots):
        snapshot_data = []
        
        for snapshot in snapshots:
            snapshot_data.append({
                'name': snapshot.name,
                'description': snapshot.description,
                'create_time': snapshot.createTime,
                'state': snapshot.state
            })
            snapshot_data += self._list_snapshots(snapshot.childSnapshotList)
        
        return snapshot_data


class VMDeviceInfoManager:

    def __init__(self, server_instance=None, content=None, vm=None):
        self._server_instance = server_instance
        self._content = content
        self._vm = vm
    
    @property
    def vm(self):
        return self._vm
    
    @vm.setter
    def vm(self, vm):
        self._vm = vm

    def _get_resource_pool(self, datacenter, cluster_name, resource_pool_name=None):
        if cluster_name:
            cluster = self._get_device([vim.ComputeResource], cluster_name, folder=datacenter)
            if not cluster:
                raise RuntimeError("Get Cluter Failed!!!")
        else:
            cluster = None

        # get resource pools limiting search to cluster or datacenter
        if resource_pool_name:
            resource_pool = self._get_device([vim.ResourcePool], resource_pool_name, folder=cluster or datacenter)
        else:
            resource_pool = cluster.resourcePool

        return resource_pool

    def build_without_device_info(self, vm_name, dc_name, cluster_name, ds_name, cpu_num, memory_num, guest_id='rhel6_64Guest', version='vmx-09'):
        try:
            data_center = self._get_device([vim.Datacenter], dc_name)
            # resource_pool = data_center.hostFolder.childEntity[0].resourcePool
            resource_pool = self._get_resource_pool(data_center, cluster_name)
            datastore_path = '[' + ds_name + ']' + vm_name   # TODO 写死的datastore1需要修改

            vmx_file = vim.vm.FileInfo(
                logDirectory=None,
                snapshotDirectory=None,
                suspendDirectory=None,
                vmPathName=datastore_path
            )

            build_config = vim.vm.ConfigSpec(
                name=vm_name,
                memoryMB=memory_num,
                numCPUs=cpu_num,
                files=vmx_file,
                guestId=guest_id,
                version=version
            )

            build_task = data_center.vmFolder.CreateVM_Task(config=build_config, pool=resource_pool)
            WaitForTask(build_task)
            self.vm = self._get_device([vim.VirtualMachine], vm_name)
        except Exception as e:
            return False, e
        
        return True, None

    def add_disk(self, d_size, d_type):
        try:
            controller = vim.vm.device.ParaVirtualSCSIController()
            controller.sharedBus = vim.vm.device.VirtualSCSIController.Sharing.noSharing
        
            virtual_device_spec = vim.vm.device.VirtualDeviceSpec()
            virtual_device_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            virtual_device_spec.device = controller

            config_spec = vim.vm.ConfigSpec()
            config_spec.deviceChange = [virtual_device_spec]

            WaitForTask(self.vm.ReconfigVM_Task(config_spec))

            # 判断已连接设备量上限
            unit_number = 0
            for dev in self.vm.config.hardware.device:
                if hasattr(dev.backing, 'fileName'):
                    unit_number = int(dev.unitNumber) + 1
                    if unit_number == 7:
                        unit_number += 1
                    if unit_number >= 16:
                        raise Exception("we don't support this many disks")
                
                if isinstance(dev, vim.vm.device.VirtualSCSIController):
                    controller = dev

            disk_spec = vim.vm.device.VirtualDeviceSpec()
            disk_spec.fileOperation = 'create'
            disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            disk_spec.device = vim.vm.device.VirtualDisk()
            disk_spec.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
            if d_type == 'thin':
                disk_spec.device.backing.thinProvisioned = True
            disk_spec.device.backing.diskMode = 'persistent'
            disk_spec.device.unitNumber = unit_number
            disk_spec.device.capacityInKB = int(d_size) * 1024 * 1024
            disk_spec.device.controllerKey = controller.key

            config_spec = vim.vm.ConfigSpec()
            config_spec.deviceChange = [disk_spec, ]

            WaitForTask(self.vm.ReconfigVM_Task(spec=config_spec))
        except Exception as e:
            return False, e
        
        return True, None

    def add_to_vswitch_portgroup(self, network_name):
        try:
            nic_spec = vim.vm.device.VirtualDeviceSpec()
            nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            nic_spec.device = vim.vm.device.VirtualE1000()
            nic_spec.device.deviceInfo = vim.Description()
            nic_spec.device.deviceInfo.summary = 'vCenter API test'  # TODO
            nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
            nic_spec.device.connectable.startConnected = True
            nic_spec.device.connectable.allowGuestControl = True
            nic_spec.device.connectable.connected = False
            nic_spec.device.connectable.status = 'untried'
            nic_spec.device.wakeOnLanEnabled = True
            nic_spec.device.addressType = 'assigned'

            network_device = self._get_device([vim.Network], network_name)
            if isinstance(network_device, vim.OpaqueNetwork):
                nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.OpaqueNetworkBackingInfo()  
                nic_spec.device.backing.opaqueNetworkType = network_device.summary.opaqueNetworkType
                nic_spec.device.backing.opaqueNetworkId = network_device.summary.opaqueNetworkId
            else:
                nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
                nic_spec.device.backing.useAutoDetect = False
                nic_spec.device.backing.deviceName = network_device.name

            network_config_spec = vim.vm.ConfigSpec()
            network_config_spec.deviceChange = [nic_spec,]

            WaitForTask(self.vm.ReconfigVM_Task(spec=network_config_spec))
        except Exception as e:
            return False, e
        
        return True, None

    def add_to_dvswitch_portgroup(self, network_name):
        try:
            # 配置虚拟的网卡
            nic_spec = vim.vm.device.VirtualDeviceSpec()
            nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            nic_spec.device = vim.vm.device.VirtualE1000()
            nic_spec.device.deviceInfo = vim.Description()
            nic_spec.device.deviceInfo.summary = 'vCenter API test'  # TODO
            nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
            nic_spec.device.connectable.startConnected = True
            nic_spec.device.connectable.allowGuestControl = True
            nic_spec.device.connectable.connected = False
            nic_spec.device.connectable.status = 'untried'
            nic_spec.device.wakeOnLanEnabled = True
            nic_spec.device.addressType = 'assigned'
            # 配置端口链接dvs端口组信息
            pg = self._get_device([vim.dvs.DistributedVirtualPortgroup], network_name)
            if not pg:
                raise RuntimeError("Not find the PortGroup")
            dvswitch = pg.config.distributedVirtualSwitch

            port = vim.dvs.PortConnection()
            port.switchUuid = dvswitch.uuid
            port.portgroupKey = pg.key
            # 配置端口连接端口组
            nic = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
            nic.port = port
            nic_spec.device.backing = nic
            # 完成网络配置
            network_config_spec = vim.vm.ConfigSpec()
            network_config_spec.deviceChange = [nic_spec,]
            WaitForTask(self.vm.ReconfigVM_Task(spec=network_config_spec))
        except Exception as e:
            return False, e
        
        return True, None

    def add_image(self, image_path, image_ds_name):
        try:
            controller = vim.vm.device.VirtualIDEController()
            for dev in self.vm.config.hardware.device:
                if isinstance(dev, vim.vm.device.VirtualIDEController):
                    controller = dev

            cd_spec = vim.vm.device.VirtualDeviceSpec()
            cd_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            cd_spec.device = vim.vm.device.VirtualCdrom()
            cd_spec.device.key = 3000
            cd_spec.device.controllerKey = controller.key
            cd_spec.device.unitNumber = 0

            cd_spec.device.deviceInfo = vim.Description()
            cd_spec.device.deviceInfo.label = 'CD/DVD drive 1'
            cd_spec.device.deviceInfo.summary = 'ISO'

            cd_spec.device.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo()
            cd_spec.device.backing.fileName = image_path

            cd_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
            cd_spec.device.connectable.startConnected = True
            cd_spec.device.connectable.allowGuestControl = True
            cd_spec.device.connectable.connected = False
            cd_spec.device.connectable.status = 'untried'

            datastore = self._get_device([vim.Datastore], image_ds_name)
            cd_spec.device.backing.datastore = datastore

            vm_conf = vim.vm.ConfigSpec()
            vm_conf.deviceChange = [cd_spec]

            WaitForTask(self.vm.ReconfigVM_Task(spec=vm_conf))
        except Exception as e:
            return False, e
        
        return True, None
    
    def update_vcpu(self, new_num_cpus, new_num_cores_per_socket=1):
        try:
            cpu_spec = vim.vm.ConfigSpec()
            cpu_spec.numCPUs = new_num_cpus
            cpu_spec.numCoresPerSocket = new_num_cores_per_socket
            WaitForTask(self.vm.ReconfigVM_Task(cpu_spec))
        except Exception as e:
            return False, e

        return True, None

    def update_mem(self, new_memory_mb):
        try:
            mem_spec = vim.vm.ConfigSpec()
            mem_spec.memoryMB = new_memory_mb

            WaitForTask(self.vm.ReconfigVM_Task(mem_spec))
        except Exception as e:
            return False, e
        
        return True, None

    def remove_network(self, nic_label):
        try:
            virtual_nic_device = None
            network_card = (vim.vm.device.VirtualEthernetCard, vim.vm.device.VirtualE1000)
            for network_dev in self.vm.config.hardware.device:
                if isinstance(network_dev, network_card) and network_dev.deviceInfo.label == nic_label:
                    virtual_nic_device = network_dev
                    break
                

            if not virtual_nic_device:
                raise Exception
            
            virtual_nic_destory_spec = vim.vm.device.VirtualDeviceSpec()
            virtual_nic_destory_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
            virtual_nic_destory_spec.device = virtual_nic_device

            destory_spec = vim.vm.ConfigSpec()
            destory_spec.deviceChange = [virtual_nic_destory_spec]
            WaitForTask(self.vm.ReconfigVM_Task(spec=destory_spec))
        except Exception as e:
            return False, e
        
        return True, None
    
    def remove_disk(self, disk_label):
        try:
            virtual_disk_device = None
            for disk_dev in self.vm.config.hardware.device:
                if isinstance(disk_dev, vim.vm.device.VirtualDisk) and disk_dev.deviceInfo.label == disk_label:
                    virtual_disk_device = disk_dev
            
            if not virtual_disk_device:
                raise Exception
            
            virtual_disk_destory_spec = vim.vm.device.VirtualDeviceSpec()
            virtual_disk_destory_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
            virtual_disk_destory_spec.device = virtual_disk_device
            virtual_disk_destory_spec.fileOperation = vim.vm.device.VirtualDeviceSpec.FileOperation.destroy
        
            destory_spec = vim.vm.ConfigSpec()
            destory_spec.deviceChange = [virtual_disk_destory_spec]
            WaitForTask(self.vm.ReconfigVM_Task(spec=destory_spec))
        except Exception as e:
            return False
        
        return True
    
    def remove_image(self, cdrom_label):
        try:
            virtual_cdrom_device = None
            for cdrom_dev in self.vm.config.hardware.device:
                if isinstance(cdrom_dev, vim.vm.device.VirtualCdrom) and cdrom_dev.deviceInfo.label == cdrom_label:
                    virtual_cdrom_device = cdrom_dev
            
            if not virtual_cdrom_device:
                raise Exception
            
            virtual_cdrom_destory_spec = vim.vm.device.VirtualDeviceSpec()
            virtual_cdrom_destory_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
            virtual_cdrom_destory_spec.device = virtual_cdrom_device
        
            destory_spec = vim.vm.ConfigSpec()
            destory_spec.deviceChange = [virtual_cdrom_destory_spec]
            WaitForTask(self.vm.ReconfigVM_Task(spec=destory_spec))
        except Exception as e:
            return False
        
        return True

    def clone(self, new_vm_name, dc_name, ds_name, rp_name, target_host_name=None):
        """
        克隆
        """
        if not ds_name:
            # raise Exception('Params Error')
            return False, "DataStore name parameter error failed"

        try:
            data_store = self._get_device([vim.Datastore], ds_name)
            if not data_store:
                raise Exception('Failed to get DataStore object')

            if dc_name:
                data_center = self._get_device([vim.Datacenter], dc_name)
            else:
                data_center = self._content.rootFolder.childEntity[0]

            vmfloder = data_center.vmFolder

            resource_pool = None
            
            if target_host_name:
                for cluster in data_center.hostFolder.childEntity:
                    for host in cluster.host:
                        if host.name == target_host_name:
                            resource_pool = cluster.resourcePool
                            break
            elif rp_name:
                resource_pool = self._get_device([vim.ResourcePool], rp_name, folder=data_center)
            else:
                resource_pool = data_center.hostFolder.childEntity[0].resourcePool

            host = self._get_device([vim.HostSystem], target_host_name)

            relospec = vim.vm.RelocateSpec()
            relospec.datastore = data_store
            if resource_pool:
                relospec.pool = resource_pool
            if host:
                relospec.host = host

            clonespec = vim.vm.CloneSpec()
            clonespec.location = relospec
            clonespec.powerOn = False

            WaitForTask(self.vm.CloneVM_Task(folder=vmfloder, name=new_vm_name, spec=clonespec))
        except Exception as e:
            return False, e.msg if hasattr(e, 'msg') else str(e)
        
        return True, None

    def ip_assignment(self):
        # TODO 待测试
        try:
            if self._vm.summary.config.name != 'poweredOff':
                raise Exception('Power off your VM before reconfigure')
            
            adaptermap = vim.vm.customization.AdapterMapping()
            adaptermap.adapter = vim.vm.customization.IPSettings()
            adaptermap.adapter.ip = vim.vm.customization.FixedIp()
            adaptermap.adapter.ip.ipAddress = ip
            adaptermap.adapter.subnetMask = subnet
            adaptermap.adapter.gateway = gateway
            # guest_map.adapter.dnsServerList = dns
            adaptermap.adapter.dnsDomain = domain if domain else 'kaopuyun.com'
            
            globalip = vim.vm.customization.GlobalIPSettings()
            globalip.dnsServerList = dns

            ident = vim.vm.customization.LinuxPrep()
            ident.domain = domain if domain else 'kaopuyun.com'
            ident.hostName=vim.vm.customization.FixedName()
            ident.hostName.name = self.vm.summary.config.name

            customspec = vim.vm.customization.Specification()
            customspec.identity = ident
            customspec.nicSettingMap = [adaptermap]
            customspec.globalIPSettings = globalip
            
            WaitForTask(self.vm.Customize(spec=customspec))
        except vmodl.MethodFault as e:
            # raise Exception('Caught vmodl fault: %s' % e.msg)
            return False
        except Exception as e:
            return False 
        
        return True

    def _get_device(self, vim_type, device_name, folder=None):
        """获取设备信息"""
        if not folder:
            folder = self._content.rootFolder

        device_info = None
        container = self._content.viewManager.CreateContainerView(
            folder, vim_type, True
        )

        for item in container.view:
            if item.name == device_name:
                device_info = item
                break
        
        container.Destroy()
        return device_info

    @staticmethod
    def get_vm_by_name(name):
        return VMDeviceInfoManager._get_device([vim.VirtualMachine], name)
