import os
import launch
import launch_ros


def generate_launch_description():

    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='hande_tutorials',
            executable='hande_service',
            parameters=[],
            name='hande_server',
            output='screen')])
