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



class RtpreemptWidget(QWidget):

    def __init__(self, node, plugin=None):

        super(RtpreemptWidget, self).__init__()

        self._node = node

        _, package_path = get_resource('packages', 'rqt_rt_preempt')
        ui_file = os.path.join(package_path, 'share', 'rqt_rt_preempt', 'resource', 'RosRtpreempt.ui')
        loadUi(ui_file, self)
         
        self._plugin = plugin
        
        self.buttonBuild.clicked.connect(self.buttonBuildPressed)
        
        
    def buttonBuildPressed(self):
        self.buttonBuild.setText('Text Changed')

    def start(self):
        pass

    def shutdown_plugin(self):
        pass


