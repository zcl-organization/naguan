from pyVmomi import vim

from app.main.vcenter.control import get_obj
from app.main.vcenter.control.vcenter import get_connect
from app.main.vcenter.db import network_port_group as db_network


def get_network_list(platform_id):
    s, content, platform = get_connect(platform_id)
    network = get_obj(content, [vim.Network], 'VM Network')

    print(network)


def get_network_by_id(id):

    return db_network.network_list_by_id(id)

