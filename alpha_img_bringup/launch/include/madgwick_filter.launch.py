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
        'madgwick_filter.yaml'
    )

    # imu/data_raw + imu/mag -> imu/data (orientation) consumed by the EKF
    node = Node(
        package='imu_filter_madgwick',
        executable='imu_filter_madgwick_node',
        name='madgwick_filter_node',
        namespace=robot_name,
        output='screen',
        parameters=[param_config]
    )

    return LaunchDescription([node])
