import os
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node


def generate_launch_description():
    robot_name = 'alpha_img'
    robot_bringup = robot_name + '_bringup'

    param_config = os.path.join(
        get_package_share_directory(robot_bringup),
        'config',
        'sensors',
        'nmea_gps.yaml'
    )

    node = Node(
        package='nmea_navsat_driver',
        executable='nmea_serial_driver',
        name='nmea_serial_driver',
        namespace=robot_name,
        output='screen',
        parameters=[param_config],
        remappings=[
            ('fix', 'gps/fix'),
            ('heading', 'gps/heading'),
            ('time_reference', 'gps/time_reference'),
            ('vel', 'gps/vel'),
        ]
    )

    return LaunchDescription([node])
