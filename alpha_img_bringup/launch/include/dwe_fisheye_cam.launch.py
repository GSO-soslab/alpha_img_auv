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
        'usb_cam.yaml'
    )

    # DWE StellarHD fisheye camera. usb_cam publishes through image_transport,
    # so image_raw/compressed is available without a separate republish node.
    node = Node(
        package='usb_cam',
        executable='usb_cam_node_exe',
        name='usb_cam',
        namespace=robot_name,
        output='screen',
        parameters=[param_config],
    )

    return LaunchDescription([node])
