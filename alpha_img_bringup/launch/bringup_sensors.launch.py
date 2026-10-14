import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    arg_robot_name = 'alpha_img'
    robot_bringup = arg_robot_name + '_bringup'

    def include(name):
        return IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch', 'include', name)]),
            launch_arguments = {'arg_robot_name': arg_robot_name}.items()
        )

    # Microstrain AHRS (imu/data_raw, imu/mag)
    imu = include('microstrain.launch.py')

    # Madgwick filter (imu/data_raw + imu/mag -> imu/data)
    madgwick = include('madgwick_filter.launch.py')

    # Waterlinked DVL
    dvl = include('waterlinked_dvl.launch.py')

    # Bluerobotics Bar30 pressure sensor
    pressure = include('bluerobotics_bar30.launch.py')

    # GPS (NMEA over serial)
    gps = include('gps_nmea.launch.py')

    return LaunchDescription([
        imu,
        madgwick,
        dvl,
        pressure,
        gps,
    ])
