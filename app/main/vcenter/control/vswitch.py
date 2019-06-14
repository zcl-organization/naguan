# -*- coding: utf-8 -*-
import json   # TODO 序列化方式变更不用json
from app.main.vcenter import db
from app.main.vcenter.utils.base import VCenter
from app.main.vcenter.utils.vm_vswitch import VMVswitchManager
from app.main.vcenter.control.utils import get_mor_name


def sync_vswitch(vswitch_datas, platform_id):
    """
    同步数据
    """
    if not vswitch_datas:
        return
    
    local_data = {(item.name, item.host_name): item.id for item in db.vswitch.vswitch_all(platform_id)}
    for vswitch, host in vswitch_datas:
        nics = [item for item in vswitch.spec.policy.nicTeaming.nicOrder.activeNic]
        data = {
            "platform_id": platform_id, 
            "name": vswitch.name, 
            "mor_name": '', # get_mor_name(vswitch)  TODO 获取mor_name的方式或是直接取消
            "host_name": host.name,
            "host_mor_name": get_mor_name(host), 
            "mtu": vswitch.mtu, 
            "num_of_port": vswitch.numPorts, 
            "nics": json.dumps(nics)
        }
        if (vswitch.name, host.name) in local_data.keys():
            data['vswitch_id'] = local_data[(vswitch.name, host.name)]
            db.vswitch.vswitch_update(**data)
            local_data.pop((vswitch.name, host.name))
        else:
            db.vswitch.vswitch_create(**data)

    for item in local_data.values():
        db.vswitch.vswitch_delete(item)


def get_vswitch_infos(platform_id):
    """
    获取本地所有的vswitch信息
    """
    vswitchs = db.vswitch.vswitch_all(platform_id)
    vswitch_list = []

    for vswitch in vswitchs:
        vs_item = dict(vswitch)

        vswitch_list.append(vs_item)

    return vswitch_list


def check_if_vswitch_exists(vswitch_id=None, platform_id=None, host_name=None, switch_name=None):
    """
    检查vswitch是否存在
    """
    if vswitch_id:
        return True if db.vswitch.find_vswitch_by_id(vswitch_id) else False
    elif platform_id and host_name and switch_name:
        return True if db.vswitch.find_vswitch_by_name(platform_id, host_name, switch_name) else False
    else:
        raise RuntimeError("Check Failed!!!")


class VSwitch:

    def __init__(self, platform_id):
        self._platform_id = platform_id
        self._vcenter = VCenter(platform_id)

    def create_vswitch(self, args):
        """
        创建vswitch
        """
        if check_if_vswitch_exists(
            platform_id=args['platform_id'], host_name=args['host_name'], switch_name=args['switch_name']):
            raise RuntimeError("Project Already Exists!!!")

        mtu=args['mtu'] if args['mtu'] else 1500,
        num_port=args['num_port'] if args['num_port'] else 128,
        nics=args['nics'] if args['nics'] else []

        hostsystem = self._vcenter.find_hostsystem_by_name(args['host_name'])

        vmvsm = VMVswitchManager(hostsystem)
        if not vmvsm.create(args['switch_name'], num_port, mtu, nics):
            raise RuntimeError("Create VSwitch Failed!!!")
        
        # TODO 同步
    
    def delete_vswitch_by_name(self, host_name, switch_name):
        """
        通过名称组（host， switch）删除vswitch
        """
        hostsystem = self._vcenter.find_hostsystem_by_name(host_name)
        vmvsm = VMVswitchManager(hostsystem)
        if not vmvsm.destroy(switch_name):
            raise RuntimeError("Destroy VSwitch Failed!!!")

    def delete_vswitch_by_id(self, vswitch_id):
        """
        通过标识id删除vswitch
        """
        data = db.vswitch.find_vswitch_by_id(vswitch_id)
        if not data:
            raise RuntimeError("Project Does Not Exists!!!")

        self.delete_vswitch_by_name(data.host_name, data.name)

        # TODO  同步

    def update_vswich(self, args, switch_id):
        """
        更新vswitch
        """
        data = db.vswitch.find_vswitch_by_id(switch_id)
        if not data:
            raise RuntimeError('Project Does Not Exists!!!')

        old_data = dict(
            mtu=data.mtu,
            num_ports=data.num_of_port,
            pnic=json.loads(data.nics)
        )
        nics = nics if nics else []

        hostsystem = self._vcenter.find_hostsystem_by_name(args['host_name'])
        vmvsm = VMVswitchManager(hostsystem)
        
        if not vmvsm.update(args['switch_name'], old_data, args['num_port'], args['mtu'], args['nics']):
            raise RuntimeError("Updata VSwitch Failed!!!")
        
        # TODO 同步