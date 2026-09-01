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
    rslidar_ros_dir = get_package_share_directory("rslidar_sdk")
    scout_base_dir = get_package_share_directory('scout_base')
    scout_bringup_dir = get_package_share_directory('scout_bringup')
    pointcloud_to_laserscan_ros_dir = get_package_share_directory('pointcloud_to_laserscan')

    driver_node = Node(
            package='rslidar_sdk',
            executable='rslidar_sdk_node',
            name='rslidar_sdk_node',
            output='screen',)


    base_link_to_laser_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_base_laser_rslidar',
        arguments=['0','0','0.26','0','0','0','1','base_link','rslidar']
    )
    scanner = DeclareLaunchArgument(
            name='scanner', default_value='scanner',
            description='Namespace for sample topics'
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
    dummy_pointcloud_publisher=Node(
            package='pointcloud_to_laserscan', executable='dummy_pointcloud_publisher',
            remappings=[('cloud', [LaunchConfiguration(variable_name='scanner'), '/cloud'])],
            parameters=[{'cloud_frame_id': 'cloud', 'cloud_extent': 2.0, 'cloud_size': 500}],
            name='cloud_publisher'
        )
    pointcloud_to_laserscan_node=Node(
            package='pointcloud_to_laserscan', 
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            remappings=[('cloud_in','/rslidar_points'),
                        ('scan', '/scan')],
            parameters=[{
                'target_frame': 'rslidar',
                'transform_tolerance': 0.01,
                'min_height': -0.35,
                'max_height': 0.5,
                'angle_min': -3.1415,  # -M_PI/2
                'angle_max': 3.1415,  # M_PI/2
                'angle_increment': 0.0087,  # M_PI/360.0
                'scan_time': 0.1,
                'range_min': 0.1,
                'range_max': 20.0,
                'use_inf': True,
                'inf_epsilon': 1.0
            }],
            
        )

    return LaunchDescription([
        IncludeLaunchDescription(
             PythonLaunchDescriptionSource([scout_base_dir,'/launch','/scout_mini_base.launch.py']),
         ),  
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([rf2o_dir,'/launch','/rf2o_laser_odometry.launch.py']),
        # ),
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([rslidar_ros_dir,'/launch','/start.py']),
        # ),
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([pointcloud_to_laserscan_ros_dir,'/launch','/sample_pointcloud_to_laserscan_launch.py']),
        # ),
        driver_node,
        scanner,
        base_link_to_laser_tf_node,
        rf2o,
        dummy_pointcloud_publisher,
        pointcloud_to_laserscan_node
    ])
