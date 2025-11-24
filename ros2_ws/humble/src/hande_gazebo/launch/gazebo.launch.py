# hande_gazebo/launch/hande_gazebo.launch.py

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

import xacro


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time", default="true")

    hande_description_share = get_package_share_directory("hande_description")
    xacro_file = os.path.join(hande_description_share, "urdf", "hande.urdf.xacro")
    doc = xacro.process_file(
        xacro_file,
        mappings={
            "robot_name": "hande",
            "mode": "gazebo",
        },
    )
    robot_description_xml = doc.toxml()
    robot_description = {"robot_description": robot_description_xml}

    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            robot_description,
            {"use_sim_time": use_sim_time},
        ],
    )

    world = PathJoinSubstitution(
        [
            FindPackageShare("hande_gazebo"),
            "worlds",
            "hande_world.sdf",
        ]
    )

    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("ros_gz_sim"),
                    "launch",
                    "gz_sim.launch.py",
                ]
            )
        ),
        launch_arguments={"gz_args": world}.items(),
    )

    clock_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock]"],
        output="screen",
    )

    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-string", robot_description_xml,
            "-allow_renaming",
            "-z", "0.01",
        ],
        output="screen",
    )

    jsb_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "controller_manager",
        ],
        output="screen",
    )

    hande_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "hande_controller",
            "--controller-manager",
            "controller_manager",
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
                description="Use simulation clock if true",
            ),
            gz_sim_launch,
            clock_bridge,
            rsp,
            spawn,
            jsb_spawner,
            hande_spawner,
        ]
    )
