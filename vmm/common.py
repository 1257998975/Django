# -*- coding: utf-8 -*-
from django.http import HttpResponse

# 导入vSphere SDK模块
import atexit
from pyVmomi import vim
from pyVim import connect
from vmm.models import vms
from vmm.forms import vm_regist
from django.shortcuts import render
from pyVim.connect import SmartConnect, Disconnect
from django.template import loader, Context


# 虚拟机电源管理
def vmpower(request):
    uuid = request.GET.get('uuid')
    op_type = request.GET.get('type')
    print (op_type)
    try:
        si = connect.SmartConnectNoSSL(host="172.16.3.141",
                                       user="administrator@vsphere.local",
                                       pwd="Server@2012",
                                       port=443)
    except vim.fault.InvalidLogin:
        print("Could not connect to the specified host using specified "
              "username and password")
        return -1

    atexit.register(connect.Disconnect, si)
    action = si.content.searchIndex.FindByUuid(None, uuid, True, True)
    if op_type == '0':  # 关机
        action.ShutdownGuest()
    elif op_type == '1':  # 开机
        action.PowerOn()
    elif op_type == '-1':  # 重启
        action.RebootGuest()
    return HttpResponse(op_type)


# 修改信息
def modify():
    pass


# 申请虚拟机
def applyvm():
    pass


# 创建虚拟机
def createvm(request):
    user_id = request.session.get('user_id')
    if request.session.get('user_id'):
        if request.method == 'POST':  # 当提交表单时
            vm_regist_info = vm_regist(request.POST)  # form 包含提交的数据
            if vm_regist_info.is_valid():  # 如果提交的数据合法
                print("输入数据合法！ ")
                print(vm_regist_info.cleaned_data)
            else:
                print("输入数据不合法！")
                print(vm_regist_info.cleaned_data)
        else:  # 当正常访问时
            vm_regist_info = vm_regist()
        tp = loader.get_template("backend/createvm.html")
        html = tp.render()
        return HttpResponse(html)
        # return render(request, 'vmm/templates/backend/createvm.html', {'form': vm_regist_info})
    else:
        return HttpResponse("你还未登录，点击<a href=\"/login/\">这里</a>登录!")

        # 克隆虚拟机


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

    # set relospec
    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = resource_pool

    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.powerOn = power_on

    print("cloning VM...")
    task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
    wait_for_task(task)


def creat(request):
    """
    Let this thing fly
    """
    # connect this thing
    si = connect.SmartConnectNoSSL(
        host="172.16.3.141",
        user="administrator@vsphere.local",
        pwd="Server@2012",
        port=443)
    # disconnect this thing
    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    template = None

    template = get_obj(content, [vim.VirtualMachine], "WinXP")

    if template:
        clone_vm(
            content, template, "xx", si,
            "", "",
            "", "",
            "", 1)
        return HttpResponse("完成")
    else:
        return HttpResponse("template not found")
