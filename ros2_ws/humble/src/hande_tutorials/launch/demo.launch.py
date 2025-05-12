import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    urdf_file_name = 'urdf/hande.urdf'
    urdf = os.path.join(
        get_package_share_directory('hande_tutorials'),
        urdf_file_name)
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation clock if true'),
        DeclareLaunchArgument(
            name='is_sim',
            default_value='false',
            description='True if running in simulation'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
            arguments=[urdf]),
        Node(
            package='hande_tutorials',
            executable='hande_service',
            parameters=[{'is_sim': LaunchConfiguration('is_sim')}],
            name='hande_server',
            output='screen'),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=[
                '-d', '/ros2_ws/install/hande_tutorials/share/hande_tutorials/rviz/demo.rviz'])
    ])
