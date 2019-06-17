# -*- coding:utf-8 -*-
from pyVim.task import WaitForTask
from pyVmomi import vim
from app.main.vcenter import db
from app.main.vcenter.control.utils import get_obj, get_connect, get_obj_by_mor_name, get_mor_name


class InstanceTemplate:

    def __init__(self, platform_id, uuid):
        self.si, self.content, self.platform = get_connect(platform_id)
        template = db.instances.list_by_uuid(platform_id, uuid)  # 数据库模板
        self.platform_id, self.uuid = platform_id, uuid
        self.template_name = template.vm_name
        self.template = get_obj(self.content, [vim.VirtualMachine], self.template_name)  # 模板文件

    # host_id 未做
    def template_create_vm(self, new_vm_name, ds_id, dc_id, resource_pool_id=None, host_id=None):
        if not self.template:
            raise ValueError('The template does not exist.')
        if not self.template.summary.config.template:
            raise Exception('Object are not template')
        datastore = self.get_ds(ds_id)
        data_center, vmfloder = self.get_dc_and_vmfloder(dc_id)
        resource_pool = self.get_resource_pool(resource_pool_id=resource_pool_id,
                                               host_id=host_id, data_center=data_center)
        # 判断是否存在同名虚拟机
        for vm in resource_pool.vm:
            if new_vm_name == vm.name:
                raise ValueError('Existing vm names')
        # RelocateSpec
        relospec = vim.vm.RelocateSpec()
        relospec.datastore = datastore
        relospec.pool = resource_pool

        # ConfigSpec
        configSpec = vim.vm.ConfigSpec()
        configSpec.annotation = "This is a create from the template"  ##

        # CloneSpec
        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec
        clonespec.powerOn = False
        clonespec.config = configSpec

        print ("Templates create vm...")
        # 执行
        WaitForTask(self.template.Clone(folder=vmfloder, name=new_vm_name, spec=clonespec))
        # 同步
        for vm in resource_pool.vm:
            if new_vm_name == vm.name:
                self.sync_instance(vm)
                break

    def get_ds(self, ds_id):
        ds_info = db.datastores.get_ds_by_id(ds_id)
        if not ds_info:
            raise Exception('Unable to get DataStore')
        data_store = get_obj(self.content, [vim.Datastore], ds_info.ds_name)  # 数据存储
        if not data_store:
            raise Exception('Unable to Get DataStore')
        return data_store

    def get_dc_and_vmfloder(self, dc_id):
        dc_info = db.vcenter.vcenter_tree_by_id(dc_id)
        if dc_info.name:
            data_center = get_obj(self.content, [vim.Datacenter], dc_info.name)  # 数据中心
        else:
            data_center = self.content.rootFolder.childEntity[0]
        vmfloder = data_center.vmFolder  #
        return data_center, vmfloder

    def get_resource_pool(self, resource_pool_id=None, host_id=None, data_center=None):
        rp_mor_name = None
        host_name = None
        if resource_pool_id:
            rp_mor_name = db.resource_pool.get_resource_pool_mor_name_by_id(resource_pool_id)
        elif host_id:
            host_name = None   # 未做

        resource_pool = None
        if rp_mor_name:
            resource_pool = get_obj_by_mor_name(self.content, [vim.ResourcePool], rp_mor_name)
        elif host_name:
            for cluster in data_center.hostFolder.childEntity:
                for host in cluster.host:
                    if host.name == host_name:
                        resource_pool = cluster.resourcePool
                        break
        else:
            resource_pool = data_center.hostFolder.childEntity[0].resourcePool
        return resource_pool

    def sync_instance(self, vm):
        if vm.summary.guest is not None:
            ip = vm.summary.guest.ipAddress
        else:
            ip = ''
        if vm.resourcePool:
            resource_pool_name = vm.resourcePool.name
            # db.instances.update_vm_rp_name_by_vm_mor_name(platform['id'], get_mor_name(vm), vm.resourcePool.name)
        else:
            resource_pool_name = None

        db.instances.vcenter_vm_create(uuid=vm.summary.config.uuid, platform_id=self.platform_id,
                                       vm_name=vm.summary.config.name,
                                       vm_mor_name=get_mor_name(vm), template=vm.summary.config.template,
                                       vm_path_name=vm.summary.config.vmPathName,
                                       memory=vm.summary.config.memorySizeMB,
                                       cpu=vm.summary.config.numCpu,
                                       num_ethernet_cards=vm.summary.config.numEthernetCards,
                                       num_virtual_disks=vm.summary.config.numVirtualDisks,
                                       instance_uuid=vm.summary.config.instanceUuid,
                                       guest_id=vm.summary.config.guestId,
                                       guest_full_name=vm.summary.config.guestFullName,
                                       host=vm.summary.runtime.host.name, ip=ip, status=vm.summary.runtime.powerState,
                                       resource_pool_name=resource_pool_name, created_at=vm.config.createDate)

    def template_transform_vm(self, resource_pool_id=None, host_id=None):
        # MarkAsVirtualMachine
        # data_center = self.template.datastore[0].parent.parent
        if not self.template:
            raise ValueError('The template does not exist.')
        if not self.template.summary.config.template:
            raise Exception('Object are not template')
        resource_pool = self.get_resource_pool(resource_pool_id=resource_pool_id,
                                               host_id=None, data_center=None)
        print ("Template transform vm...")
        # 执行
        self.template.MarkAsVirtualMachine(pool=resource_pool)  # host未做
        # 同步
        self.sync_template_transform_vm(resource_pool.name)

    def sync_template_transform_vm(self, resource_pool_name):
        db.instances.vcenter_sync_template_transform_vm(self.platform_id, self.uuid, resource_pool_name)

    def del_template(self):
        if self.template:
            if self.template.summary.config.template:
                WaitForTask(self.template.Destroy())
                # 同步
                self.sync_del_template()
            else:
                raise Exception('Object are not template')
        else:
            raise ValueError('Template does not exist.')

    def sync_del_template(self):
        db.instances.del_template(self.platform_id, self.uuid)
