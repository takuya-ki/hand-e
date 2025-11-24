# hande_control/launch/hande_control.launch.py

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

import xacro


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time", default="false")

    hande_description_share = get_package_share_directory("hande_description")
    xacro_file = os.path.join(hande_description_share, "urdf", "hande.urdf.xacro")
    doc = xacro.process_file(xacro_file, mappings={"use_gazebo": "false"})
    robot_desc = doc.toxml()

    # hande_control の controllers yaml
    hande_control_share = get_package_share_directory("hande_control")
    controllers_yaml = os.path.join(
        hande_control_share, "config", "hande_controllers.yaml"
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation clock if true",
            ),

            # robot_state_publisher
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="hande_robot_state_publisher",
                output="screen",
                parameters=[
                    {
                        "use_sim_time": use_sim_time,
                        "robot_description": robot_desc,
                    }
                ],
                remappings=[("/joint_states", "/hande/joint_states")],
            ),

            # ros2_control_node (FakeSystem or ros2_control hardware)
            Node(
                package="controller_manager",
                executable="ros2_control_node",
                # name="controller_manager",
                output="screen",
                parameters=[
                    {"use_sim_time": use_sim_time},
                    {"robot_description": robot_desc},
                    controllers_yaml,
                ],
            ),

            # joint_state_broadcaster
            Node(
                package="controller_manager",
                executable="spawner",
                name="hande_joint_state_broadcaster_spawner",
                arguments=["joint_state_broadcaster", "-c", "controller_manager"],
                output="screen",
            ),

            # hande_controller (JointTrajectoryController)
            Node(
                package="controller_manager",
                executable="spawner",
                name="hande_controller_spawner",
                arguments=["hande_controller", "-c", "controller_manager"],
                output="screen",
            ),
        ]
    )
