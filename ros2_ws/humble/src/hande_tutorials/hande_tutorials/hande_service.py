#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from robotiq_modbus_controller.driver import RobotiqModbusRtuDriver


class CloseOpenDemonstrator(Node):

    def __init__(self):
        super().__init__('hande_server')
        self.device = "/dev/ttyUSB0"
        self.driver = RobotiqModbusRtuDriver(self.device)
        self.driver.connect()
        self.driver.reset()
        self.driver.activate()

    def closeopen(self, pos_val):
        """ Excutes a demonstration. """

        self.get_logger().info("pos_val: " + str(pos_val))
        self.driver.move(pos=pos_val, speed=64, force=1)


def main(args=None):
    rclpy.init(args=args)
    demo_node = CloseOpenDemonstrator()

    demo_node.get_logger().info("Start demonstrating.")

    cur_pos_val = 255  # maximum
    while rclpy.ok():
        cur_pos_val = 255 - cur_pos_val
        demo_node.closeopen(pos_val=cur_pos_val)
        rclpy.spin_once(demo_node, timeout_sec=3.0)

    demo_node.get_logger().info("End demonstrating.")
    demo_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
