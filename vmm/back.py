# -*- coding: utf-8 -*-
# 导入vSphere SDK模块
import atexit
import time
from vmm.class_ob import CloneData_ob
from vmm.class_ob import ob_vs
from django.http import HttpResponse
from django.template import loader
from pyVim import connect
from pyVim.connect import Disconnect
from pyVmomi import vim
from vmm.model.models import vms
from vmm.model.token import Token
from vmm.model.forms import vm_regist
from django.conf import settings
from vmm.model.models import users


# -------------------------------------------------------------------------------------------------
# 创建虚拟机
def wait_for_task(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            print("there was an error")
            task_done = True


def get_obj(content, vimtype, name):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    return obj


def clone_vm(
        content, template, vm_name, si,
        datacenter_name, vm_folder, datastore_name,
        cluster_name, resource_pool, power_on):
    """
    Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
    cluster_name, resource_pool, and power_on are all optional.
    """
    # if none git the first one
    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)

    if vm_folder:
        destfolder = get_obj(content, [vim.Folder], vm_folder)
    else:
        destfolder = datacenter.vmFolder

    if datastore_name:
        datastore = get_obj(content, [vim.Datastore], datastore_name)
    else:
        datastore = get_obj(
            content, [vim.Datastore], template.datastore[0].info.name)

    # if None, get the first one
    cluster = get_obj(content, [vim.ClusterComputeResource], cluster_name)

    if resource_pool:
        resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)
    else:
        resource_pool = cluster.resourcePool

    print(resource_pool)

    # set relospec
    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = resource_pool

    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.powerOn = power_on
    task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
    wait_for_task(task)


def creat(vm):
    os = vm.vm_os
    name = vm.vm_name
    """
    Let this thing fly
    """
    # connect this thing
    # disconnect this thing
    ob_vs.vmlist()
    # db_info_renew = vms.objects.get(user_id=input_id)

    content = ob_vs.si.RetrieveContent()
    template = None

    template = get_obj(content, [vim.VirtualMachine], os)
    if template:
        x = clone_vm(
            content, template, name, ob_vs.si,
            CloneData_ob.datacenter_name, CloneData_ob.vm_folder,
            CloneData_ob.datastore_name, CloneData_ob.cluster_name,
            CloneData_ob.resource_pool, CloneData_ob.power_on)
        return True
    else:
        return False


# ------------------------------------------------------------------------------------------------------------


# 修改虚拟机配置
def config(vm):
    """
    Let this thing fly
    """
    # connect this thing
    name = vm.vm_name
    CPU = vm.vm_cpu
    memory = vm.vm_memory
    si = ob_vs.si
    # disconnect this thing
    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    container = content.rootFolder
    viewType = [vim.VirtualMachine]
    recursive = True
    containerView = content.viewManager.CreateContainerView(
        container, viewType, recursive)
    children = containerView.view
    for vms in children:
        if vms.name == name:
            numCPUs = vim.vm.ConfigSpec()
            numCPUs.numCPUs = CPU
            numCPUs.numCoresPerSocket = CPU / 2
            numCPUs.memoryMB = memory
            vms.ReconfigVM_Task(numCPUs)

            action = si.content.searchIndex.FindByUuid(None, vms.summary.config.instanceUuid, True, True)

            return True
    return False


# 更新数据库
def autoupdate(delay):
    vms_list = ob_vs.vmlist()  # 执行查找
    vm_infor = vms.objects.all()  # 获得vms表单信息
    for vml in vms_list:
        vm_ob = vms.objects.get(vm_uuid=vml.summary.config.instanceUuid)
        if (vm_ob):
            vm_ob.vm_name = vml.summary.config.name

            if (vml.guest.guestFamily == "windowsGuest"):
                vm_ob.vm_os = "Windows"
                vm_ob.vm_os_admin = 1
            elif(vml.guest.guestFamily ==None):
                vm_ob.vm_os = None
                vm_ob.vm_os_admin = 0
            else:
                vm_ob.vm_os = "Linux"
                vm_ob.vm_os_admin = 0
            vm_ob.vm_type = 0
            vm_ob.vm_ip = vml.summary.guest.ipAddress
            vm_ob.vm_cpu = vml.summary.runtime.maxCpuUsage
            vm_ob.vm_memory = vml.summary.runtime.maxMemoryUsage
            if (len(vml.summary.runtime.powerState) > 9):
                vm_ob.vm_power = 0
            else:
                vm_ob.vm_power = 1
            vm_ob.save()
        else:
            if (len(vml.summary.runtime.powerState) > 9):
                a_vm_power = 0
            else:
                a_vm_power = 1
            if (vml.guest.guestFamily == "windowsGuest"):
                a_vm_os = "Windows"
                a_vm_admin = 1
            else:
                a_vm_os = "Linux"
                a_vm_admin = 0
            vms.objects.create(vm_user_id="root", vm_name=vml.summary.config.name,
                               vm_os=a_vm_os, vm_cpu=vml.summary.runtime.maxCpuUsage,
                               vm_memory=vml.summary.runtime.maxMemoryUsage,
                               vm_os_admin=a_vm_admin, vm_type=0, vm_ip=vml.summary.guest.ipAddress,
                               vm_uuid=vml.summary.config.instanceUuid,vm_power=a_vm_power)
    for vmi in vm_infor:
        k = False
        for vml in vms_list:
            if (vml.summary.config.instanceUuid == vmi.vm_uuid):
                k = True
                continue
        if (not k):
            vmi.delete()

# def print_time( delay):
#     count = 0
#     while count < 5:
#         time.sleep(delay)
#         count += 1
#         print (1)
