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
        
        subprocess.run(["mkdir", "-p", self.lineEditBuildDir.text()])
        
        subprocess.run(["wget", "-P", self.lineEditBuildDir.text(), self.lineEditRtpreemptPatch.text()])
        
        subprocess.run(["wget", "-P", self.lineEditBuildDir.text(), self.lineEditLinuxKernel.text()])

    def start(self):
        pass

    def shutdown_plugin(self):
        pass


