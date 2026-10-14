from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression
from launch.actions import SetEnvironmentVariable
from launch.actions import TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
import os

def generate_launch_description():

    # Node argument
    robot_name = LaunchConfiguration('robot_name')
    localization_delay = LaunchConfiguration('localization_delay')

    # Node param
    localization_param_file = Path(
        get_package_share_directory('alpha_img_bringup'), 
        'config/localization/robot_localization.yaml'
    )
     

    # Robot_Localization node
    localization = Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            namespace=robot_name,
            # output='screen',
            parameters=[localization_param_file],
            emulate_tty=True        
    )

    return LaunchDescription([

        # Decalre arguments
        DeclareLaunchArgument(
            'robot_name', default_value = 'my_robot'            
        ),

        DeclareLaunchArgument(
            'localization_delay', default_value = '0.0'            
        ),

        # Delay the node if needed
        TimerAction(
            period=PythonExpression([localization_delay]),
            actions=[localization]
        ),
    ])