#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState
from robotiq_modbus_controller.driver import RobotiqModbusRtuDriver


class CloseOpenDemonstrator(Node):

    def __init__(self):
        super().__init__('closeopen_demonstrator')

        self.declare_parameter('is_real', False)
        self.is_real = self.get_parameter('is_real').get_parameter_value().bool_value

        if self.is_real:
            self.device = "/dev/ttyUSB0"
            self.driver = RobotiqModbusRtuDriver(self.device)
            self.driver.connect()
            self.driver.reset()
            self.driver.activate()

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, '/hande/joint_states', qos_profile)

    def closeopen(self, pos_val):
        """ Excutes a demonstration. """

        if self.is_real:
            pos_val_real = pos_val * 255.0
            self.get_logger().info("Current position value (real): " + str(pos_val_real))
            self.driver.move(pos=int(pos_val_real), speed=64, force=1)

        pos_val_sim = pos_val * 0.025
        self.get_logger().info("Current position value (pos_val): " + str(pos_val_sim))
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


def main(args=None):
    rclpy.init(args=args)
    demo_node = CloseOpenDemonstrator()

    demo_node.get_logger().info("Start demonstrating.")

    cur_pos_val = 1.0  # Maximum
    while rclpy.ok():
        cur_pos_val = 1.0 - cur_pos_val
        demo_node.closeopen(pos_val=cur_pos_val)
        rclpy.spin_once(demo_node, timeout_sec=3.0)

    demo_node.get_logger().info("End demonstrating.")
    demo_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
