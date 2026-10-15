import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def launch_setup(context, *args, **kwargs):
    arg_robot_name = 'alpha_img'
    robot_bringup = arg_robot_name + '_bringup'

    def include(name):
        return IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch', 'include', name)]),
            launch_arguments = {'arg_robot_name': arg_robot_name}.items()
        )

    dvl_choice = LaunchConfiguration('dvl').perform(context)
    gps_choice = LaunchConfiguration('gps').perform(context)

    dvl_files = {
        'waterlinked': 'waterlinked_dvl.launch.py',
        'nortek': 'nortek_dvl.launch.py',
    }
    gps_files = {
        'nmea': 'gps_nmea.launch.py',
        'unicore': 'unicore_rtk.launch.py',
        'gpsd': 'gps_gpsd.launch.py',
    }
    if dvl_choice not in dvl_files:
        raise RuntimeError(f"dvl must be one of {list(dvl_files)}, got '{dvl_choice}'")
    if gps_choice not in gps_files:
        raise RuntimeError(f"gps must be one of {list(gps_files)}, got '{gps_choice}'")

    return [
        # Microstrain AHRS (imu/data_raw, imu/mag)
        include('microstrain.launch.py'),
        # Madgwick filter (imu/data_raw + imu/mag -> imu/data)
        include('madgwick_filter.launch.py'),
        # DVL: Waterlinked (default) or Nortek Nucleus
        include(dvl_files[dvl_choice]),
        # Bluerobotics Bar30 pressure sensor
        include('bluerobotics_bar30.launch.py'),
        # GPS: NMEA over serial (default), Unicore RTK, or gpsd
        include(gps_files[gps_choice]),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('dvl', default_value='waterlinked',
                              description="DVL driver: 'waterlinked' or 'nortek'"),
        DeclareLaunchArgument('gps', default_value='nmea',
                              description="GPS driver: 'nmea', 'unicore' (RTK) or 'gpsd'"),
        OpaqueFunction(function=launch_setup),
    ])
