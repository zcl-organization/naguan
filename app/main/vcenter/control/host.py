# -*- coding:utf-8 -*-
import hashlib
import socket
import ssl
from pyVmomi import vim
from app.main.vcenter.control.utils import get_connect, get_obj


class Host:
    def __init__(self, platform_id):
        self.si, self.content, self.platform = get_connect(platform_id)

    def add_host(self, host_name, esxi_username, esxi_password):
        host = get_obj(self.content, [vim.HostSystem], host_name)
        """Add ESXi host to a cluster of folder in vCenter"""
        changed = True
        result = None

        host_connect_spec = self.get_host_connect_spec(esxi_hostname=host_name, esxi_username=esxi_username,
                                                       esxi_password=esxi_password)
        as_connected = self.params.get('add_connected')
        esxi_license = None
        resource_pool = None
        task = None
        if folder_name:
            self.folder = search_folder(folder_name)
            try:
                task = self.folder.AddStandaloneHost(
                    spec=host_connect_spec, compResSpec=resource_pool,
                    addConnected=as_connected, license=esxi_license
                )
            except Exception as e:
                pass
        elif self.cluster_name:
            self.host, self.cluster = self.search_cluster(
                self.datacenter_name,
                self.cluster_name,
                self.esxi_hostname
            )

        try:
            changed, result = wait_for_task(task)
            result = "Host connected to vCenter '%s'" % self.vcenter
        except TaskError as task_error:
            self.module.fail_json(
                msg="Failed to add host to vCenter '%s' : %s" % (self.vcenter, to_native(task_error))
            )

        self.module.exit_json(changed=changed, result=result)

    def get_host_connect_spec(self, esxi_hostname, esxi_username, esxi_password,
                              force_connection=None, fetch_ssl_thumbprint=None,
                              esxi_ssl_thumbprint=None):
        """
        Returns: host connection specification
        """
        host_connect_spec = vim.host.ConnectSpec()
        host_connect_spec.hostName = esxi_hostname
        host_connect_spec.userName = esxi_username
        host_connect_spec.password = esxi_password
        host_connect_spec.force = force_connection
        # Get the thumbprint of the SSL certificate
        if fetch_ssl_thumbprint and esxi_ssl_thumbprint == '':
            # We need to grab the thumbprint manually because it's not included in
            # the task error via an SSLVerifyFault exception anymore
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            wrapped_socket = ssl.wrap_socket(sock)
            try:
                wrapped_socket.connect((esxi_hostname, 443))
            except socket.error as socket_error:
                return "Cannot connect to host : %s" % socket_error
            else:
                der_cert_bin = wrapped_socket.getpeercert(True)
                # thumb_md5 = hashlib.md5(der_cert_bin).hexdigest()
                thumb_sha1 = self.format_number(hashlib.sha1(der_cert_bin).hexdigest())
                # thumb_sha256 = hashlib.sha256(der_cert_bin).hexdigest()
            wrapped_socket.close()
            host_connect_spec.sslThumbprint = thumb_sha1
        else:
            host_connect_spec.sslThumbprint = esxi_ssl_thumbprint
        return host_connect_spec

    @staticmethod
    def format_number(number):
        """Format number"""
        string = str(number)
        return ':'.join(a + b for a, b in zip(string[::2], string[1::2]))
