#!/usr/bin/env python3

import time
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState
from hande_interfaces.srv import SetCommand
from robotiq_modbus_controller.driver import RobotiqModbusRtuDriver


class HandeServer(Node):

    def __init__(self):
        super().__init__('hande_command_server')

        self.declare_parameter('is_sim', False)
        self.is_sim = self.get_parameter('is_sim').get_parameter_value().bool_value
        self.pos_val = 0.0

        if not self.is_sim:
            self.device = "/dev/ttyUSB0"
            self.driver = RobotiqModbusRtuDriver(self.device)
            self.driver.connect()
            self.driver.reset()
            self.driver.activate()
            self.driver.move(pos=int(255.0), speed=64, force=1)
        else:
            qos_profile = QoSProfile(depth=10)
            self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
            joint_state = JointState()
            try:
                # update joint_state
                now = self.get_clock().now()
                joint_state.header.stamp = now.to_msg()
                joint_state.name = ['hande_left_finger_joint']
                joint_state.position = [0.025]
                # send the joint state and transform
                self.joint_pub.publish(joint_state)
            except KeyboardInterrupt:
                pass

        self.set_command_srv = self.create_service(
            SetCommand,
            "/hande/set_command",
            self.hande_set_command)

    def hande_set_command(self, request, response):
        """To handle sending commands via socket connection."""
        self.get_logger().info(request.command)
        pos_val = self.genCommand(request.command)

        if not self.is_sim:
            pos_val *= 255.0
            self.get_logger().info("Current position value: " + str(pos_val))
            self.driver.move(pos=int(pos_val), speed=64, force=1)
        else:
            pos_val *= 0.025
            self.get_logger().info("Current position value: " + str(pos_val))
            joint_state = JointState()
            try:
                # update joint_state
                now = self.get_clock().now()
                joint_state.header.stamp = now.to_msg()
                joint_state.name = ['hande_left_finger_joint']
                joint_state.position = [pos_val]
                # send the joint state and transform
                self.joint_pub.publish(joint_state)
            except KeyboardInterrupt:
                pass

        time.sleep(1)
        return response

    def genCommand(self, command):
        """Updates the command according to the character entered by the user."""    

        # close
        if command == 'c':
            self.pos_val = 1.0

        # open
        if command == 'o':
            self.pos_val = 0.0   

        # (0-255): go to that position
        # If the command entered is a int, assign this value to rPRA
        try: 
            self.pos_val = int(command)
            if self.pos_val > 1.0:
                self.pos_val = 1.0
            if self.pos_val < 0.0:
                self.pos_val = 0.0
        except ValueError:
            pass

        return self.pos_val


def main(args=None):
    rclpy.init(args=args)
    node = HandeServer()

    while rclpy.ok():
        rclpy.spin_once(node)

    node.destroy_service(node.set_command_srv)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
