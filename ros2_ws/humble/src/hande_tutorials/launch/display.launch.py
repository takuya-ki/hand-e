from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ld = LaunchDescription()

    hande_tutorials_path = FindPackageShare('hande_tutorials')
    default_model_path = PathJoinSubstitution(['urdf', 'hande.urdf.xacro'])
    default_rviz_config_path = PathJoinSubstitution([hande_tutorials_path, 'rviz', 'urdf.rviz'])

    # These parameters are maintained for backwards compatibility
    ld.add_action(DeclareLaunchArgument(
        name='gui',
        default_value='true',
        choices=['true', 'false'],
        description='Flag to enable joint_state_publisher_gui'
    ))
    ld.add_action(DeclareLaunchArgument(
        name='rvizconfig',
        default_value=default_rviz_config_path,
        description='Absolute path to rviz config file'
    ))

    # This parameter has changed its meaning slightly from previous versions
    ld.add_action(DeclareLaunchArgument(
        name='model',
        default_value=default_model_path,
        description='Path to robot urdf file relative to hande_tutorials package'
    ))
    ld.add_action(IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('urdf_launch'), 'launch', 'display.launch.py']),
        launch_arguments={
            'urdf_package': 'hande_tutorials',
            'urdf_package_path': LaunchConfiguration('model'),
            'rviz_config': LaunchConfiguration('rvizconfig'),
            'jsp_gui': LaunchConfiguration('gui')}.items()
    ))

    return ld
