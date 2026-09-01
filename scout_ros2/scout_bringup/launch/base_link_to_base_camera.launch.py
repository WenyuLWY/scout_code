from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    base_link_to_camera_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_base_camera',
        arguments=[
            '0.27','0','0.0',
            '-1.57','0.0','-1.57',
            'base_link',
            'camera_car_color_optical_frame'
        ]
    )

    return LaunchDescription([
        base_link_to_camera_node
    ])
