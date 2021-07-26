#!/usr/bin/env python

from __future__ import division

import itertools
import os

from ament_index_python import get_resource
from python_qt_binding import loadUi
from python_qt_binding.QtCore import Qt, QTimer, qWarning, Slot
from python_qt_binding.QtGui import QIcon
from python_qt_binding.QtWidgets import QHeaderView, QMenu, QTreeWidgetItem, QWidget
from rqt_py_common.message_helpers import get_message_class

import subprocess



class RtpreemptWidget(QWidget):

    def __init__(self, node, plugin=None):

        super(RtpreemptWidget, self).__init__()

        self._node = node

        _, package_path = get_resource('packages', 'rqt_rt_preempt')
        ui_file = os.path.join(package_path, 'share', 'rqt_rt_preempt', 'resource', 'RosRtpreempt.ui')
        loadUi(ui_file, self)
         
        self._plugin = plugin
        
        self.buttonBuild.clicked.connect(self.buttonBuildPressed)
        
        self.lineEditRtpreemptPatch.setText("http://cdn.kernel.org/pub/linux/kernel/projects/rt/5.10/patch-5.10.52-rt47.patch.gz")
        self.lineEditLinuxKernel.setText("https://mirrors.edge.kernel.org/pub/linux/kernel/v5.x/linux-5.10.52.tar.gz")
        # self.lineEditBuildDir.setText("/home/ros2/rt-preempt-kernel/5.10.52/")
        self.lineEditBuildDir.setText("/tmp/haaa")
        
    def buttonBuildPressed(self):
        self.buttonBuild.setText('Text Changed')
        
        if not os.path.isdir(self.lineEditBuildDir.text()):
            os.makedirs(self.lineEditBuildDir.text())
            self.plainTextEditLog.setPlainText("Created Build Directory: " + self.lineEditBuildDir.text())
        else:
            self.plainTextEditLog.setPlainText("Build Directory already exists: " + self.lineEditBuildDir.text())
        
        # self.plainTextEditLog.setPlainText("Downloading: " + self.lineEditRtpreemptPatch.text())       
        # subprocess.run(["wget", "-P", self.lineEditBuildDir.text(), self.lineEditRtpreemptPatch.text()])
        #
        # self.plainTextEditLog.setPlainText("Downloading: " + self.lineEditLinuxKernel.text())
        # subprocess.run(["wget", "-P", self.lineEditBuildDir.text(), self.lineEditLinuxKernel.text()])
        #
        # self.plainTextEditLog.setPlainText("Extracting: " + self.lineEditRtpreemptPatch.text())
        # subprocess.run(["gunzip", self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditRtpreemptPatch.text()) ])
        #
        # self.plainTextEditLog.setPlainText("Extracting: " + self.lineEditLinuxKernel.text())
        # subprocess.run(["tar", "-xzf", self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()), "-C",  self.lineEditBuildDir.text()])
        #

        self.plainTextEditLog.setPlainText("Patching linux kernel")
        output = subprocess.run(["patch", "-d", self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditLinuxKernel.text()).rstrip(".tar.gz"), "-p1", '< ' + self.lineEditBuildDir.text() + '/' + os.path.basename(self.lineEditRtpreemptPatch.text()).rstrip('.gz')],  capture_output=True)
        
        print(output)
        self.plainTextEditLog.setPlainText("hey:" )

    def start(self):
        pass

    def shutdown_plugin(self):
        pass


