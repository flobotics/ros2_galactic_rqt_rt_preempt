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
        self.process  = QProcess(self)
        self._plugin = plugin

        _, package_path = get_resource('packages', 'rqt_rt_preempt')
        ui_file = os.path.join(package_path, 'share', 'rqt_rt_preempt', 'resource', 'RosRtpreempt.ui')
        loadUi(ui_file, self)
         
        
        
        self.buttonDownloadConfigure.clicked.connect(self.buttonDownloadConfigureClicked)
        self.buttonMakeMenuconfig.clicked.connect(self.buttonMakeMenuconfigClicked)
        self.buttonBuild.clicked.connect(self.buttonBuildClicked)
        self.buttonInstall.clicked.connect(self.buttonInstallClicked)
        
        self.lineEditRtpreemptPatch.setText("http://cdn.kernel.org/pub/linux/kernel/projects/rt/5.10/patch-5.10.52-rt47.patch.gz")
        self.lineEditLinuxKernel.setText("https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/linux-5.10.52.tar.gz")
        # self.lineEditBuildDir.setText("/home/ros2/rt-preempt-kernel/5.10.52/")
        self.lineEditBuildDir.setText("/tmp/haaa")
        self.lineEditKernelConfig.setText("/boot/config-5.8.0-63-generic")
        
        # Get running linux version and display it
        current_linux_version = subprocess.run(["uname", "-mrs"], capture_output=True)
        self.labelCurrentRunningKernel.setText("Current running kernel: " + current_linux_version.stdout.decode('utf-8'))
        
        self.setHelpText()
     
    def buttonMakeMenuconfigClicked(self):
        self.process.start( 'gnome-terminal', ['--working-directory', self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()).rstrip(".tar.gz"), '-e', 'make menuconfig'])
        
    
    def buttonInstallClicked(self):
        print("buttonInstallClicked:")
        wdir = self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()).rstrip(".tar.gz")
        self.process.start( 'gnome-terminal', ['--working-directory', wdir, '-e', "sudo make modules_install"])
        self.process.start( 'gnome-terminal', ['--working-directory', wdir, '-e', "sudo make install"])
    
    def buttonBuildClicked(self):
        wdir = self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()).rstrip(".tar.gz")
        #self.process.start( 'gnome-terminal', ['--working-directory', wdir, '-e', "make -j `nproc`"])
        self.process.start( 'gnome-terminal', ['--working-directory', wdir, '-e', "make -j 128"])
     
        
    def buttonDownloadConfigureClicked(self):

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
        
        # if testIsPackageInstalled writes some logs, the user NEED to install first
        if len(self._logText) > 0:
            return
        
        if not os.path.isdir(self.lineEditBuildDir.text()):
            os.makedirs(self.lineEditBuildDir.text())
            self.setLogText("->Created Build Directory: " + self.lineEditBuildDir.text())
        else:
            self.setLogText("->Build Directory already exists: " + self.lineEditBuildDir.text())
            
        
        self.setLogText("->Downloading: " + self.lineEditRtpreemptPatch.text())   
        subprocess.run(["wget", "-P", self.lineEditBuildDir.text(), self.lineEditRtpreemptPatch.text()])
        
        self.setLogText("->Downloading: " + self.lineEditLinuxKernel.text())
        subprocess.run(["wget", "-P", self.lineEditBuildDir.text(), self.lineEditLinuxKernel.text()])
        
        self.setLogText("->Extracting: " + self.lineEditRtpreemptPatch.text())
        subprocess.run(["gunzip", self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditRtpreemptPatch.text()) ])
        
        self.setLogText("->Extracting: " + self.lineEditLinuxKernel.text())
        subprocess.run(["tar", "-xzf", self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()), "-C",  self.lineEditBuildDir.text()])
        
        self.setLogText("->Patching linux kernel: " + self.lineEditLinuxKernel.text())
        output = os.system("patch -d " + self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()).rstrip(".tar.gz") + " -p1 " + '< ' + self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditRtpreemptPatch.text()).rstrip('.gz'))
        
        self.setLogText("->Copying " + self.lineEditKernelConfig.text())  
        subprocess.run(["cp", self.lineEditKernelConfig.text() , self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()).rstrip(".tar.gz") + "/.config"])
        
        self.setLogText("->Configure kernel")
        os.system("yes '' | make oldconfig -C" + self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()).rstrip(".tar.gz"))


        
    def setLogText(self, txt):
        self._logText += txt + '\n'
        self.plainTextEditLog.setPlainText(self._logText)
           

    def testIsPackageInstalled(self, name):
        output = subprocess.run(["dpkg", "-l", name ],  capture_output=True)
        dpkg_output = output.stdout.decode('utf-8').split('\n')
        dpkg_output_line = dpkg_output[len(dpkg_output) - 2]
        if not dpkg_output_line.startswith('ii'):
            self.setLogText("->Install " + name + " and try it again. sudo apt install " + name)
            # self._logText += "->Install " + name + " and try it again. sudo apt install " + name + '\n'
            # self.plainTextEditLog.setPlainText(self._logText)

    def setHelpText(self):
        self.plainTextEditHelp.setPlainText("If you want to use another rt-preempt patch, look at \n\
        http://cdn.kernel.org/pub/linux/kernel/projects/rt/ and choose another one.\n\
        \n\
        For another linux kernel you can look at https://mirrors.edge.kernel.org/pub/linux/kernel/ \n\
        and choose if you want.\n\
        When running 'make menuconfig'-button, you need to setup\n\
        rt-preempt stuff. This is done with make menuconfig and not per e.g. script-insert, because there\n\
        is included more, and perhaps this changes from version to version, so configure it with make menuconfig\n\
        is the best, most universal option. You need to select in make menuconfig the following \n\
        --> Enable CONFIG_PREEMPT_RT \n\
            -> General Setup \n\
                -> Preemption Model (Fully Preemptible Kernel (Real-Time)) \n\
                    (X) Fully Preemptible Kernel (Real-Time)) \n\
        \n\
        --> Enable CONFIG_HIGH_RES_TIMERS \n\
            -> General setup \n\
                -> Timers subsystem \n\
                    [*] High Resolution Timer Support \n\
         \n\
        --> Enable CONFIG_NO_HZ_FULL \n\
            -> General setup \n\
                -> Timers subsystem \n\
                    -> Timer tick handling (Full dynticks system (tickless)) \n\
                        (X) Full dynticks system (tickless)            \n\
         \n\
        --> Set CONFIG_HZ_1000 (note: this is no longer in the General Setup menu, go back twice) \n\
            -> Processor type and features \n\
                -> Timer frequency (1000 HZ) \n\
                    (X) 1000 HZ            \n\
         \n\
        --> Set CPU_FREQ_DEFAULT_GOV_PERFORMANCE [=y] \n\
            ->  Power management and ACPI options \n\
                -> CPU Frequency scaling \n\
                    -> CPU Frequency scaling (CPU_FREQ [=y]) \n\
                        -> Default CPUFreq governor (<choice> [=y]) \n\
                            (X) performance \n\
        ")
                       
        
        
        
    def start(self):
        pass

    def shutdown_plugin(self):
        pass


