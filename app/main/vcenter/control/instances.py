# -*- coding:utf-8 -*-
from pyVim import connect
import atexit

from pyVmomi import vmodl
from pyVmomi import vim

from app.main.vcenter.control import get_mor_name, wait_for_tasks

from app.main.vcenter.db import instances as db_vm
from app.main.vcenter.control.vcenter import get_connect


def vm_list_all(platform_id, host, vm_name):
    vms = db_vm.vm_list(platform_id, host, vm_name)
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
    return vm_list


def get_obj(content, vimtype, moc_name):
    """
     Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        # print(c)
        # get_mor_name
        if get_mor_name(c) == moc_name:
            obj = c
            break
    return obj


def power_action(action, platform_id, uuid):
    s, content, platfrom = get_connect(platform_id)

    vm = db_vm.vm_list_by_uuid(platfrom['id'], uuid)
    vm_mor_name = vm.vm_mor_name
    vm = get_obj(content, [vim.VirtualMachine], vm_mor_name)

    # print(vm)
    force = True
    if action == 'start':
        # invoke_and_track(vm.PowerOn, None)
        task = vm.PowerOn()
        wait_for_tasks(s, [task])

    elif action == 'stop':
        if not force:
            task = vm.ShutdownGuest()
            wait_for_tasks(s, [task])
            # invoke_and_track(vm.ShutdownGuest)
            # wait_for_tasks(s, vm.ShutdownGuest)
        else:
            task = vm.PowerOff()
            wait_for_tasks(s, [task])
            # invoke_and_track(vm.PowerOff)

    elif action == 'suspend':
        if not force:
            task = vm.StandbyGuest()
            wait_for_tasks(s, [task])
        else:
            task = vm.Suspend()
            wait_for_tasks(s, [task])
    elif action == 'restart':
        task = vm.ResetVM_Task()
        wait_for_tasks(s, [task])


def vm_delete(platform_id, uuid):
    s, content, platfrom = get_connect(platform_id)

    # print(platform_id,uuid)
    local_vm = db_vm.vm_list_by_uuid(platfrom['id'], uuid)
    vm_mor_name = local_vm.vm_mor_name
    vm = get_obj(content, [vim.VirtualMachine], vm_mor_name)

    # print("The current powerState is: {0}".format(vm.runtime.powerState))
    # print("Attempting to power off {0}".format(vm.name))
    # task = vm.PowerOff()
    # wait_for_tasks(s, [task])

    # print("{0}".format(task.info.state))
    # print("The current powerState is: {0}".format(vm.runtime.powerState))
    # print("Destroying VM from vSphere.")

    # task = vm.Destroy_Task()
    # print(dir(vm))
    task = vm.Destroy()
    wait_for_tasks(s, [task])
    print("Done.")
    # 从数据库中删除云主机及 user_instance
    # pass


def vm_update_cpu(platform_id, uuid, new_cpu, old_cpu):
    s, content, platfrom = get_connect(platform_id)

    local_vm = db_vm.vm_list_by_uuid(platfrom['id'], uuid)

    if local_vm.cpu == old_cpu:
        vm_mor_name = local_vm.vm_mor_name
        vm = get_obj(content, [vim.VirtualMachine], vm_mor_name)

        cspec = vim.vm.ConfigSpec()
        cspec.numCPUs = int(new_cpu)
        cspec.numCoresPerSocket = 1
        task = vm.Reconfigure(cspec)
        wait_for_tasks(s, [task])
        print('update success cpu')
    else:
        raise Exception('参数错误')


def vm_update_memory(platform_id, uuid, new_memory, old_memory):
    s, content, platfrom = get_connect(platform_id)

    local_vm = db_vm.vm_list_by_uuid(platfrom['id'], uuid)

    if local_vm.memory == old_memory:
        vm_mor_name = local_vm.vm_mor_name
        vm = get_obj(content, [vim.VirtualMachine], vm_mor_name)

        cspec = vim.vm.ConfigSpec()
        cspec.memoryMB = int(new_memory)
        task = vm.Reconfigure(cspec)
        wait_for_tasks(s, [task])
        print('update success memory')
    else:
        raise Exception('参数错误')
