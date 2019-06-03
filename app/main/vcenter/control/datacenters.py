from pyVmomi import vim
from app.main.vcenter.control.instances import Instance


def create_datacenter(platform_id, dc_name, folder=None):
    instance = Instance(platform_id)
    si = instance.si

    if len(dc_name) > 79:
        raise ValueError("The name of the datacenter must be under "
                         "80 characters.")

    if folder is None:
        folder = si.content.rootFolder

    if folder is not None and isinstance(folder, vim.Folder):
        dc_moref = folder.CreateDatacenter(name=dc_name)
        return dc_moref


def create_cluster(datacenter, cluster_name, cluster_spec=None):
    """
    Method to create a Cluster in vCenter
    :param kwargs:
    :return: Cluster MORef
    """
    if datacenter is None:
        raise ValueError("Missing value for datacenter.")
    if cluster_name is None:
        raise ValueError("Missing value for name.")
    if cluster_spec is None:
        cluster_spec = vim.cluster.ConfigSpecEx()

    host_folder = datacenter.hostFolder
    cluster = host_folder.CreateClusterEx(name=cluster_name, spec=cluster_spec)
    return cluster
