import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    robot_name = 'alpha_img'
    robot_bringup = robot_name + '_bringup'

    # DWE StellarHD fisheye camera
    camera = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch', 'include', 'dwe_fisheye_cam.launch.py')]),
        launch_arguments = {'robot_name': robot_name}.items()
    )

    return LaunchDescription([camera])
