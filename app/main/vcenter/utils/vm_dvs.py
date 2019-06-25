# -*- coding: utf-8 -*-
from pyVmomi import vim
from pyVim.task import WaitForTask


class VMDvswitchManager:
    def __init__(self, connect, folder=None, datacenter=None):
        self._connect = connect
        self._folder = folder
        self._datacenter = datacenter

    def create(self, **kwargs):
        """
        创建Dvswitch
        TODO 管理员信息配置和描述
        """
        need_args = [
            "switch_name",  # 端口组名称
            "mtu",    # mtu数据
            "discovery_protocol",  # 发现协议配置类型  'cdp', 'lldp'
            "discovery_operation", # 发现协议配置操作  'both', 'advertise', 'listen'
            "uplink_quantity",   # 上行链路组数量
            "uplink_prefix",   # 上行链路组前缀名称
            "switch_version",  # 交换机版本信息  '5.0.0', '5.1.0', '5.5.0', '6.0.0', '6.5.0', '6.6.0'
        ]
        self._check_need_args(kwargs, need_args)

        spec = vim.DistributedVirtualSwitch.CreateSpec()
        spec.configSpec = vim.dvs.VmwareDistributedVirtualSwitch.ConfigSpec()
        spec.configSpec.name = kwargs['switch_name']
        spec.configSpec.maxMtu = kwargs['mtu']
        # 配置发现协议相关
        ldp_config_spec = vim.host.LinkDiscoveryProtocolConfig()
        ldp_config_spec.protocol = kwargs['discovery_protocol']
        ldp_config_spec.operation = kwargs['discovery_operation']
        spec.configSpec.linkDiscoveryProtocolConfig = ldp_config_spec
        # 配置上行链路组名称
        spec.configSpec.uplinkPortPolicy = vim.DistributedVirtualSwitch.NameArrayUplinkPortPolicy()
        for count in range(1, kwargs['uplink_quantity'] + 1):
            spec.configSpec.uplinkPortPolicy.uplinkPortName.append("%s%d" % (kwargs['uplink_prefix'], count))
        # 配置交换机版本信息
        product_info_spec = vim.dvs.ProductSpec()
        product_info_spec.version = kwargs['switch_version']
        spec.productInfo = product_info_spec

        try:
            WaitForTask(self._folder.CreateDVS_Task(spec))
        except Exception as e:
            return False
        
        return True

    def destroy(self, switch_name):
        folder = self._folder if self._folder else self._datacenter.networkFolder
        dvs = self._get_object([vim.DistributedVirtualSwitch], switch_name, folder)

        try:
            WaitForTask(dvs.Destroy_Task())
        except Exception as e:
            return False
        
        return True

    def update_mtu(self, switch_name, mtu):
        dvs = self._get_object([vim.DistributedVirtualSwitch], switch_name, self._folder)

        if mtu and dvs.config.maxMtu != mtu:
            config_spec = vim.dvs.VmwareDistributedVirtualSwitch.ConfigSpec()
            config_spec.configVersion = dvs.config.configVersion
            config_spec.maxMtu = mtu
            try:
                WaitForTask(dvs.ReconfigureDvs_Task(config_spec))
            except Exception as e:
                return False  # 修改失败
            
            return True  # 修改成功
        
        return False  # 无修改

    def update_link_protocol(self, switch_name, protocol, operation):
        dvs = self._get_object([vim.DistributedVirtualSwitch], switch_name, self._folder)

        # 修改发现协议
        ldp_protocol = dvs.config.linkDiscoveryProtocolConfig.protocol
        ldp_operation = dvs.config.linkDiscoveryProtocolConfig.operation
        if protocol and operation and (ldp_protocol != protocol or ldp_operation != operation):
            config_spec = vim.dvs.VmwareDistributedVirtualSwitch.ConfigSpec()
            config_spec.configVersion = dvs.config.configVersion
            
            ldp_config_spec = vim.host.LinkDiscoveryProtocolConfig()
            ldp_config_spec.protocol = protocol
            ldp_config_spec.operation = operation
            config_spec.linkDiscoveryProtocolConfig = ldp_config_spec

            try:
                WaitForTask(dvs.ReconfigureDvs_Task(config_spec))
            except Exception as e:
                return False  # 修改失败
            
            return True  # 修改成功
        
        return False  # 无修改

    def update_uplink_name(self, switch_name, operation, old_uplink_name, new_uplink_name):
        dvs = self._get_object([vim.DistributedVirtualSwitch], switch_name, self._folder)
        
        config_spec = vim.dvs.VmwareDistributedVirtualSwitch.ConfigSpec()
        config_spec.configVersion = dvs.config.configVersion
        config_spec.uplinkPortPolicy = vim.DistributedVirtualSwitch.NameArrayUplinkPortPolicy()
        if operation == "update":  # 修改旧的数据
            for uplink_port_name in dvs.config.uplinkPortPolicy.uplinkPortName:
                append_name = new_uplink_name if uplink_port_name == old_uplink_name else uplink_port_name
                config_spec.uplinkPortPolicy.uplinkPortName.append(append_name)
        elif operation == "remove":  # 删除旧的数据
            for uplink_port_name in dvs.config.uplinkPortPolicy.uplinkPortName:
                if uplink_port_name == old_uplink_name:
                    continue
                config_spec.uplinkPortPolicy.uplinkPortName.append(uplink_port_name)
        elif operation == "add":  # 添加新数据
            for uplink_port_name in dvs.config.uplinkPortPolicy.uplinkPortName:
                config_spec.uplinkPortPolicy.uplinkPortName.append(uplink_port_name)
            config_spec.uplinkPortPolicy.uplinkPortName.append(new_uplink_name)
        else:
            # raise Exception("Parameter Error!!!") 
            return False

        try:
            WaitForTask(dvs.ReconfigureDvs_Task(config_spec))
        except Exception as e:
            return False  # 修改失败
        
        return True

    def update_switch_version(self, switch_name, switch_version):
        dvs = self._get_object([vim.DistributedVirtualSwitch], switch_name, self._folder)

        if switch_version and dvs.config.productInfo.version != switch_version:
            product_info_spec = vim.dvs.ProductSpec()
            product_info_spec.version = switch_version
            spec_product = product_info_spec
            try:
                WaitForTask(dvs.PerformDvsProductSpecOperation_Task("upgrade", product_info_spec))
            except Exception as e:
                print e
                return False
            
            return True

        return False 

    def _check_need_args(self, args, needs):
        """
        简单的参数检查工作
        """
        for item in needs:
            if item not in args.keys():
                raise ValueError('Parameter Error!')

    def _get_object(self, vim_type, name, folder):
        if not folder:
            folder = self._connect.rootFolder
            
        container = self._connect.viewManager.CreateContainerView(folder, vim_type, True)
        for managed_object_ref in container.view:
            if managed_object_ref.name == name:
                return managed_object_ref

        return None


class VMDvswitchHostManager:
    def __init__(self, dvs):
        self._dvs = dvs
    
    def add(self, host, vmnics=[]):
        return self._modify('add', host, vmnics)

    def edit(self, host, vmnics=[]):
        return self._modify('edit', host, vmnics)

    def remove(self, host):
        return self._modify('remove', host)

    def _modify(self, operation, host, vmnics=[]):
        spec = vim.DistributedVirtualSwitch.ConfigSpec()
        spec.configVersion = self._dvs.config.configVersion
        spec.host = [vim.dvs.HostMember.ConfigSpec()]
        spec.host[0].operation = operation
        spec.host[0].host = host

        if operation in ("edit", "add"):
            spec.host[0].backing = vim.dvs.HostMember.PnicBacking()
            count = 0

            for nic in vmnics:
                spec.host[0].backing.pnicSpec.append(vim.dvs.HostMember.PnicSpec())
                spec.host[0].backing.pnicSpec[count].pnicDevice = nic
                uplink_pg = self._dvs.config.uplinkPortgroup[0] if len(self._dvs.config.uplinkPortgroup) else None
                spec.host[0].backing.pnicSpec[count].uplinkPortgroupKey = uplink_pg.key
                count += 1

        try:
            WaitForTask(self._dvs.ReconfigureDvs_Task(spec))
        except Exception as e:
            return False

        return True
