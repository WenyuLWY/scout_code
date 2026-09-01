from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('piper_serial', default_value='_261322072862'),
        DeclareLaunchArgument('car_serial', default_value='_261222076171'),

  
        #左边摄像头
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')]),
            launch_arguments={'serial_no': LaunchConfiguration('piper_serial'),
                            'camera_namespace': "",
                            'camera_name': "camera_piper",
                            'rgb_camera.color_profile': '640,480,30', 
                            'depth_module.color_profile': '640,480,30', 
                            'depth_module.depth_profile': '640,480,30',
                            'depth_module.infra_profile': '640,480,30'}.items()
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')]),
            launch_arguments={'serial_no': LaunchConfiguration('car_serial'),
                            'camera_namespace': "",
                            'camera_name': "camera_car",
                            'rgb_camera.color_profile': '640,480,30', 
                            'depth_module.color_profile': '640,480,30', 
                            'depth_module.depth_profile': '640,480,30',
                            'depth_module.infra_profile': '640,480,30'}.items()
        )
    ])

