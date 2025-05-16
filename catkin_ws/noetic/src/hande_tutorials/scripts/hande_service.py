#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
from hande_interfaces.srv import SetCommand, SetCommandResponse
from robotiq_modbus_controller.driver import RobotiqModbusRtuDriver


class HandeServer:
    def __init__(self):
        rospy.init_node('hande_command_server')

        self.is_real = rospy.get_param('~is_real', False)
        self.pos_val = 0.0

        if self.is_real:
            self.device = "/dev/ttyUSB0"
            self.driver = RobotiqModbusRtuDriver(self.device)
            self.driver.connect()
            self.driver.reset()
            self.driver.activate()
            self.driver.move(pos=int(255.0), speed=64, force=1)

        self.joint_pub = rospy.Publisher('joint_states', JointState, queue_size=10)

        joint_state = JointState()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = ['hande_left_finger_joint']
        joint_state.position = [0.025]
        self.joint_pub.publish(joint_state)

        self.service = rospy.Service('/hande/set_command', SetCommand, self.hande_set_command)

        rospy.loginfo("HandeServer ready.")

    def hande_set_command(self, req):
        rospy.loginfo("Received command: %s", req.command)
        pos_val = self.gen_command(req.command)

        if self.is_real:
            pos_val_real = pos_val * 255.0
            rospy.loginfo("Moving real hand to pos: %d", int(pos_val_real))
            self.driver.move(pos=int(pos_val_real), speed=64, force=1)

        pos_val_sim = pos_val * 0.025
        rospy.loginfo("Publishing simulated joint state: %.3f", pos_val_sim)

        joint_state = JointState()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = ['hande_left_finger_joint']
        joint_state.position = [pos_val_sim]
        self.joint_pub.publish(joint_state)

        return SetCommandResponse()

    def gen_command(self, command_str):
        try:
            if command_str == 'c':
                self.pos_val = 1.0
            elif command_str == 'o':
                self.pos_val = 0.0
            else:
                val = float(command_str)
                self.pos_val = min(max(val, 0.0), 1.0)
        except ValueError:
            rospy.logwarn("Invalid command: %s", command_str)
        return self.pos_val


if __name__ == '__main__':
    try:
        server = HandeServer()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
