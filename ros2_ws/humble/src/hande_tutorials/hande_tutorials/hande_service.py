#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState
from hande_interfaces.srv import SetCommand
from robotiq_modbus_controller.driver import RobotiqModbusRtuDriver


class HandeServer(Node):

    def __init__(self):
        super().__init__('hande_command_server')

        self.declare_parameter('is_real', False)
        self.is_real = self.get_parameter('is_real').get_parameter_value().bool_value
        self.pos_val = 0.0

        if self.is_real:
            self.device = "/dev/ttyUSB0"
            self.driver = RobotiqModbusRtuDriver(self.device)
            self.driver.connect()
            self.driver.reset()
            self.driver.activate()
            self.driver.move(pos=int(255.0), speed=64, force=1)

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, '/hande/joint_states', qos_profile)
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

        if self.is_real:
            pos_val_real = pos_val * 255.0
            self.get_logger().info("Current position value (real): " + str(pos_val_real))
            self.driver.move(pos=int(pos_val_real), speed=64, force=1)

        pos_val_sim = pos_val * 0.025
        self.get_logger().info("Current position value (sim): " + str(pos_val_sim))
        joint_state = JointState()
        try:
            # update joint_state
            now = self.get_clock().now()
            joint_state.header.stamp = now.to_msg()
            joint_state.name = ['hande_left_finger_joint']
            joint_state.position = [pos_val_sim]
            # send the joint state and transform
            self.joint_pub.publish(joint_state)
        except KeyboardInterrupt:
            pass

        response.success = True
        response.message = "Command '{}' executed.".format(request.command)
        return response

    def genCommand(self, command):
        """Updates the command according to the character entered by the user."""    

        if command == 'c':  # close
            self.pos_val = 1.0
        elif command == 'o':  # open
            self.pos_val = 0.0
        else:
            # assuming that the command is within the range of 0.0 to 1.0
            try: 
                self.pos_val = float(command)
                if self.pos_val > 1.0:
                    self.pos_val = 1.0
                elif self.pos_val < 0.0:
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
