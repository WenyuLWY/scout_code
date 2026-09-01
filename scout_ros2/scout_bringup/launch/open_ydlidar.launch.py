import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    rf2o_dir = get_package_share_directory('rf2o_laser_odometry')
    ydlidar_ros_dir = get_package_share_directory("ydlidar_ros2_driver")
    scout_base_dir = get_package_share_directory('scout_base')
    scout_bringup_dir = get_package_share_directory('scout_bringup')


    base_link_to_laser_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_base_laser_ydlidar',
        arguments=['0.2','0','0.03','0','0','0','1','base_link','laser_frame']
    )
   
    rf2o = Node(
        package='rf2o_laser_odometry',
        executable='rf2o_laser_odometry_node',
        name='rf2o_laser_odometry',
        output='screen',
        parameters=[{
            'laser_scan_topic' : '/scan',
            'odom_topic' : '/odom',
            'publish_tf' : True,
            'base_frame_id' : 'base_link',
            'odom_frame_id' : 'odom',
            'init_pose_from_topic' : '',
            'freq' : 10.0}],)

    return LaunchDescription([
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([scout_base_dir,'/launch','/scout_mini_base.launch.py']),
        # ),  
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([rf2o_dir,'/launch','/rf2o_laser_odometry.launch.py']),
        # ),
        IncludeLaunchDescription(
             PythonLaunchDescriptionSource([scout_base_dir,'/launch','/scout_mini_base.launch.py']),
         ),  
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([ydlidar_ros_dir,'/launch','/ydlidar_launch.py']),
        ),
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([scout_bringup_dir,'/launch/humble','/ekf_odom.launch.py']),
        # ), 
        # pub_tf
       # rf2o,
        base_link_to_laser_tf_node
        
    ])
