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


ob_vs = Vsphere("10.84.0.116",
                         "administrator@vsphere.local",
                         "123qweASD.",
                         443)
