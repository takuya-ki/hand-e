#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
from robotiq_modbus_controller.driver import RobotiqModbusRtuDriver


class CloseOpenDemonstrator:
    def __init__(self):
        rospy.init_node('closeopen_demonstrator')

        self.is_real = rospy.get_param('~is_real', False)
        self.is_closed = False  # Start open

        if self.is_real:
            self.driver = RobotiqModbusRtuDriver("/dev/ttyUSB0")
            self.driver.connect()
            self.driver.reset()
            self.driver.activate()

        self.joint_pub = rospy.Publisher('/hande/joint_states', JointState, queue_size=10)

        # Toggle and publish every 3 seconds
        self.timer = rospy.Timer(rospy.Duration(3.0), self.toggle_and_publish)

        rospy.loginfo("CloseOpenDemonstrator initialized.")

    def toggle_and_publish(self, event):
        """Toggle state and publish corresponding joint state."""
        self.is_closed = not self.is_closed
        pos_val = 0.025 if self.is_closed else 0.0

        if self.is_real:
            raw_val = 255 if self.is_closed else 0
            rospy.loginfo("Sending real command: %d", raw_val)
            self.driver.move(pos=raw_val, speed=64, force=1)

        # Publish simulated joint states
        joint_state = JointState()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = ['hande_left_finger_joint']
        joint_state.position = [pos_val]
        self.joint_pub.publish(joint_state)

        rospy.loginfo("Published simulated joint state: %.3f", pos_val)


def main():
    try:
        CloseOpenDemonstrator()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass


if __name__ == '__main__':
    main()