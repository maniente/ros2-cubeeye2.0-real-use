import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node, ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    pkg_share = get_package_share_directory('cubeeye_camera')
    config_file_path = os.path.join(pkg_share, 'config', 'configurazione.yaml')

    # 1. Nodo Hardware Camera
    cubeeye_node = Node(
        package='cubeeye_camera',
        executable='cubeeye_camera_node',
        name='cubeeye_camera_node',
        output='screen',
        parameters=[config_file_path]
    )

    # 2. TRASFORMAZIONE STATICA: pcl -> depth
    # Argomenti: x y z yaw pitch roll parent_frame child_frame
    # Rotazione: -1.5708 rad (-90°) su Z, 0 su Y, -1.5708 rad (-90°) su X
    tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='pcl_to_depth_tf',
        arguments=['0', '0', '0', '-1.5708', '0', '-1.5708', 'pcl', 'depth']
    )

   # 3. Container per l'elaborazione (image_proc + depth_image_proc)
    image_pipeline_container = ComposableNodeContainer(
        name='image_pipeline_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            ComposableNode(
                package='image_proc',
                plugin='image_proc::RectifyNode',
                name='rectify_depth_node',
                namespace='cubeeye_camera_node',
                remappings=[
                    ('image', 'depth'),
                    ('image_rect', 'depth_rectified')
                ],
                # AGGIUNTA: Tolleranza sui timestamp e QoS dei sensori
                parameters=[{'approximate_sync': True}] 
            ),
            ComposableNode(
                package='depth_image_proc',
                plugin='depth_image_proc::PointCloudXyzNode',
                name='point_cloud_xyz_node',
                namespace='cubeeye_camera_node',
                remappings=[
                    ('image_rect', 'depth_rectified'),
                    ('camera_info', 'camera_info'),
                    ('points', 'points_from_image')
                ],
                # AGGIUNTA: Tolleranza sui timestamp
                parameters=[{'approximate_sync': True}]
            ),
        ],
        output='screen',
    )

    return LaunchDescription([
        cubeeye_node,
        tf_node,
        image_pipeline_container
    ])