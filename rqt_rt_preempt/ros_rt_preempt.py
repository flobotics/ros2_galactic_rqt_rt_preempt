from rqt_gui_py.plugin import Plugin

from .rt_preempt_widget import RtpreemptWidget
    
    
class RosRtpreempt(Plugin):


    def __init__(self, context):
        super(RosRtpreempt, self).__init__(context)
        self._node = context.node
        self._logger = self._node.get_logger().get_child('rqt_rt_preempt.ros_rt_preempt.RosRtpreempt')
        
        super(RosRtpreempt, self).__init__(context)
        self.setObjectName('RosRtpreempt')

        self._widget = RtpreemptWidget(context.node, self)

        self._widget.start()
        if context.serial_number() > 1:
            self._widget.setWindowTitle(
                self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        context.add_widget(self._widget)
