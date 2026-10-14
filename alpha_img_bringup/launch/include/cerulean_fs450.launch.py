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
        'cerulean_fs450.yaml'
    )

    def fs450(unit):
        # The driver publishes on absolute topics named after `sensor_number`
        # (/frontscan450/range, /frontscan450/range_raw). Remap them per unit so
        # two sonars do not collide.
        return Node(
            package='frontscan_ros2',
            executable='frontscan_node',
            name=unit,
            namespace=robot_name,
            output='screen',
            parameters=[param_config],
            remappings=[
                ('/frontscan450/range', '/' + robot_name + '/' + unit + '/range'),
                ('/frontscan450/range_raw', '/' + robot_name + '/' + unit + '/range_raw'),
            ]
        )

    # The driver package is not part of this repo yet, see docs/fs450.md.
    return LaunchDescription([
        fs450('fs450_port'),
        # fs450('fs450_stbd'),
    ])
