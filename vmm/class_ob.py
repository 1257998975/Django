# -*- coding: utf-8 -*-
from pyVim import connect
from pyVim.connect import Disconnect
from pyVmomi import vim
import atexit


class Vsphere(object):
    def __init__(self, host, user, pwd, port):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.si = connect.SmartConnectNoSSL(host=host,
                                            user=user,
                                            pwd=pwd,
                                            port=port)

    def vmlist(self):
        atexit.register(Disconnect, self.si)

        content = self.si.RetrieveContent()
        container = content.rootFolder
        viewType = [vim.VirtualMachine]
        recursive = True
        containerView = content.viewManager.CreateContainerView(
            container, viewType, recursive)
        children = containerView.view
        return children


ob_vs = Vsphere("10.84.0.30",
                "administrator@vsphere.local",
                "123qweASD.",
                443)


class CloneData(object):
    def __init__(self, datacenter_name, vm_folder, datastore_name, cluster_name, resource_pool, power_on):
        self.datacenter_name = datacenter_name  # 数据中心
        self.vm_folder = vm_folder
        self.datastore_name = datastore_name  # 存储
        self.cluster_name = cluster_name  # 群集
        self.resource_pool = resource_pool  # 资源池
        self.power_on = power_on  # 电源状态


CloneData_ob = CloneData("Datacenter", "",
                         "datastore1", "",
                         "11", 0)


class mysql_vm():
    def __init__(self, vm_id, vm_name, vm_uuid, vm_purpose, vm_comment, vm_os_admin, vm_os_password, vm_user_id,
                 vm_type, vm_ports, vm_ip, vm_os, vm_cpu, vm_memory, vm_disks, vm_enabled, vm_power, vm_dispose):
        self.vm_id = vm_id
        self.vm_name = vm_name
        self.vm_uuid = vm_uuid
        self.vm_purpose = vm_purpose
        self.vm_comment = vm_comment
        self.vm_os_admin = vm_os_admin
        self.vm_os_password = vm_os_password
        self.vm_user_id = vm_user_id
        self.vm_type = vm_type
        self.vm_ports = vm_ports
        self.vm_ip = vm_ip
        self.vm_os = vm_os
        self.vm_cpu = vm_cpu
        self.vm_memory = vm_memory
        self.vm_disks = vm_disks
        self.vm_enabled = vm_enabled
        self.vm_power = vm_power
        self.vm_dispose = vm_dispose
