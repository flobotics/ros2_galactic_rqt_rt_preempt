#!/usr/bin/env python

from __future__ import division

import itertools
import os

from ament_index_python import get_resource
from python_qt_binding import loadUi
from python_qt_binding.QtCore import Qt, QTimer, qWarning, Slot, QProcess
from python_qt_binding.QtGui import QIcon
from python_qt_binding.QtWidgets import QHeaderView, QMenu, QTreeWidgetItem, QWidget, QVBoxLayout
from rqt_py_common.message_helpers import get_message_class


import subprocess



class RtpreemptWidget(QWidget):

    def __init__(self, node, plugin=None):

        super(RtpreemptWidget, self).__init__()

        self._node = node
        
        self._logText = ''

        _, package_path = get_resource('packages', 'rqt_rt_preempt')
        ui_file = os.path.join(package_path, 'share', 'rqt_rt_preempt', 'resource', 'RosRtpreempt.ui')
        loadUi(ui_file, self)
         
        self._plugin = plugin
        
        self.buttonDownloadConfigure.clicked.connect(self.buttonDownloadConfigurePressed)
        
        self.lineEditRtpreemptPatch.setText("http://cdn.kernel.org/pub/linux/kernel/projects/rt/5.10/patch-5.10.52-rt47.patch.gz")
        self.lineEditLinuxKernel.setText("https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/linux-5.10.52.tar.gz")
        # self.lineEditBuildDir.setText("/home/ros2/rt-preempt-kernel/5.10.52/")
        self.lineEditBuildDir.setText("/tmp/haaa")
        self.lineEditKernelConfig.setText("/boot/config-5.8.0-63-generic")
        
     
    def buttonMakeMenuconfig(self):
        # exec("cd /tmp/haaa/linux-5.10.52 && make menuconfig")
        # exec('/bin/bash')
        self.process  = QProcess(self)
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        self.process.start(
            'xterm',
            ['-into', str(self.terminal.winId())]
        )
        
    
    def buttonInstall(self):
        pass
    
    
        
    def buttonDownloadConfigurePressed(self):
        self.buttonBuild.setText('Text Changed')

        self.testIsPackageInstalled('flex')
        self.testIsPackageInstalled('bison')
        self.testIsPackageInstalled('openssl')
        self.testIsPackageInstalled('libncurses5-dev')
        self.testIsPackageInstalled('libssl-dev')
        self.testIsPackageInstalled('dkms')
        self.testIsPackageInstalled('libelf-dev')
        self.testIsPackageInstalled('libudev-dev')
        self.testIsPackageInstalled('libpci-dev')
        self.testIsPackageInstalled('libiberty-dev')
        self.testIsPackageInstalled('autoconf')
        self.testIsPackageInstalled('fakeroot')
        
        if len(self._logText) > 0:
            return
        
        if not os.path.isdir(self.lineEditBuildDir.text()):
            os.makedirs(self.lineEditBuildDir.text())
            self._logText += "->Created Build Directory: " + self.lineEditBuildDir.text() + '\n'
            self.plainTextEditLog.setPlainText(self._logText)
        else:
            self._logText += "->Build Directory already exists: " + self.lineEditBuildDir.text() + '\n'
            # self.plainTextEditLog.setPlainText("Build Directory already exists: " + self.lineEditBuildDir.text())
            self.plainTextEditLog.setPlainText(self._logText)
        
        self._logText += "->Downloading: " + self.lineEditRtpreemptPatch.text() + '\n'
        self.plainTextEditLog.setPlainText(self._logText)       
        subprocess.run(["wget", "-P", self.lineEditBuildDir.text(), self.lineEditRtpreemptPatch.text()])
        
        self._logText += "->Downloading: " + self.lineEditLinuxKernel.text() + '\n'
        self.plainTextEditLog.setPlainText(self._logText)
        subprocess.run(["wget", "-P", self.lineEditBuildDir.text(), self.lineEditLinuxKernel.text()])
        
        self._logText += "->Extracting: " + self.lineEditRtpreemptPatch.text() + '\n'
        self.plainTextEditLog.setPlainText(self._logText)
        subprocess.run(["gunzip", self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditRtpreemptPatch.text()) ])
        
        self._logText += "->Extracting: " + self.lineEditLinuxKernel.text() + '\n'
        self.plainTextEditLog.setPlainText(self._logText)
        subprocess.run(["tar", "-xzf", self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()), "-C",  self.lineEditBuildDir.text()])
        
        self._logText += "->Patching linux kernel: " + self.lineEditLinuxKernel.text() + '\n'
        
        self.plainTextEditLog.setPlainText(self._logText)
        #output = subprocess.run(["patch", "-d", self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()).rstrip(".tar.gz"), "-p1", '< ' + self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditRtpreemptPatch.text()).rstrip('.gz')],  capture_output=True) 
        output = os.system("patch -d " + self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()).rstrip(".tar.gz") + " -p1 " + '< ' + self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditRtpreemptPatch.text()).rstrip('.gz'))
        
        # # print(output)
        # self.plainTextEditLog.setPlainText("Linux kernel patched")
        
        self._logText += "->Copying " + self.lineEditKernelConfig.text() + '\n'
        self.plainTextEditLog.setPlainText(self._logText)       
        subprocess.run(["cp", self.lineEditKernelConfig.text() , self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()).rstrip(".tar.gz") + "/.config"])
        
        self._logText += "->Configure kernel" + '\n'
        self.plainTextEditLog.setPlainText(self._logText)
        # # subprocess.run(["yes", "''", "|", "make oldconfig", "-C",  self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()).rstrip(".tar.gz")])
        os.system("yes '' | make oldconfig -C" + self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()).rstrip(".tar.gz"))


        
        

    def testIsPackageInstalled(self, name):
        output = subprocess.run(["dpkg", "-l", name ],  capture_output=True)
        dpkg_output = output.stdout.decode('utf-8').split('\n')
        dpkg_output_line = dpkg_output[len(dpkg_output) - 2]
        if not dpkg_output_line.startswith('ii'):
            self._logText += "->Install " + name + " and try it again. sudo apt install " + name + '\n'
            self.plainTextEditLog.setPlainText(self._logText)

    def start(self):
        pass

    def shutdown_plugin(self):
        pass


