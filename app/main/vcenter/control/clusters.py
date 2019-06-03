

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