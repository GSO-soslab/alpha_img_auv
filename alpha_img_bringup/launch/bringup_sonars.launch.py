import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    robot_name = 'alpha_img'
    robot_bringup = robot_name + '_bringup'

    def include(name, condition=None):
        return IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch', 'include', name)]),
            launch_arguments = {'robot_name': robot_name}.items(),
            condition=condition
        )

    arg_zenoh = DeclareLaunchArgument('zenoh', default_value='false',
                                      description='Start the rmw_zenoh router (see zenoh_setup.md)')
    arg_mbes = DeclareLaunchArgument('mbes', default_value='false',
                                     description='Start the Cerulean multibeam sonar')

    arg_fs450 = DeclareLaunchArgument('fs450', default_value='false',
                                      description='Launch the Cerulean Omniscan 450 FS driver')

    # rmw_zenoh router for multi-machine communication
    zenoh = ExecuteProcess(
        cmd=['ros2', 'run', 'rmw_zenoh_cpp', 'rmw_zenohd'],
        output='screen',
        condition=IfCondition(LaunchConfiguration('zenoh'))
    )

    # Blue Robotics Ping360 mechanically scanning imaging sonar
    msis = include('bluerobotics_ping360.launch.py')

    # Blueprint Oculus forward-looking sonar
    fls = include('blueprint_oculus_sonar.launch.py')

    # Cerulean multibeam sonar
    mbes = include('cerulean_sonar_mbes.launch.py', IfCondition(LaunchConfiguration('mbes')))

    # Cerulean Omniscan 450 FS (off by default until its Jazzy driver is available)
    fs450 = include('cerulean_fs450.launch.py', IfCondition(LaunchConfiguration('fs450')))

    return LaunchDescription([
        arg_zenoh,
        arg_mbes,
        arg_fs450,
        zenoh,
        msis,
        fls,
        mbes,
        fs450,
    ])
